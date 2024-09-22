from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    url_for,
    jsonify,
    current_app,
    request,
    session,
)
from .user_actions import UserActions


main = Blueprint("main", __name__)


def initialize_session(user):
    session.clear()
    session["user_id"] = user.id
    session["username"] = user.username
    session["email"] = user.email
    session["clicks"] = user.score_data.clicks
    session["points"] = user.score_data.points

    game_data = UserActions.get_user_game_data(user.id)
    if game_data.get("success"):
        session["user_upgrades"] = game_data["upgrades"]
        session["click_power"] = game_data["click_power"]
        session["passive_power"] = game_data["passive_power"]
    else:
        flash(game_data.get("error", "Failed to load game data. Please try again."), "error")


def flash_and_redirect(message, category="error", route="main.index"):
    flash(message, category)
    return redirect(url_for(route))


def handle_buffer_update(ignore_threshold=False):
    if not ignore_threshold:
        session["click_buffer"] = session.get("click_buffer", 0) + 1
        session["point_buffer"] = session.get("point_buffer", 0) + session.get("click_power", 1)

    if ignore_threshold or session["click_buffer"] >= current_app.config["CLICK_THRESHOLD"]:
        session["clicks"] += session["click_buffer"]
        session["points"] += session["point_buffer"]
        result = UserActions.update_user(
            session["user_id"],
            **{
                "score_data.clicks": session["clicks"],
                "score_data.points": session["points"],
            },
        )
        if result.get("success"):
            session["click_buffer"] = 0
            session["point_buffer"] = 0
        else:
            return False
    return True


@main.route("/")
def index():
    if "user_id" in session:
        game_data = {
            "username": session["username"],
            "clicks": session.get("clicks", 0) + session.get("click_buffer", 0),
            "points": session.get("points", 0) + session.get("point_buffer", 0),
            "click_power": session.get("click_power", 1),
            "passive_power": session.get("passive_power", 0),
        }

        result = UserActions.list_upgrades()
        if result.get("success"):
            upgrades = result["upgrades"]
            upgrade_data = [
                {
                    "upgrade_id": upgrade.id,
                    "name": upgrade.name,
                    "buff": (
                        f"Bonus click power: {upgrade.click_power}"
                        if upgrade.click_power != 0
                        else f"CPS bonus: {upgrade.passive_power}"
                    ),
                    "price": upgrade.price,
                    "description": upgrade.description,
                    "amount": next(
                        (
                            u["amount"]
                            for u in session["user_upgrades"]
                            if u["upgrade_id"] == upgrade.id
                        ),
                        0,
                    ),
                }
                for upgrade in upgrades
            ]
            upgrade_data = sorted(upgrade_data, key=lambda x: x["price"])
        else:
            print(result.get("error"))
            flash("Could not get upgrades.", "error")
            upgrade_data = []

        return render_template("game.html", game_data=game_data, upgrades=upgrade_data)
    else:
        return render_template("index.html")


@main.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        result = UserActions.check_password(username, password)
        if result.get("success"):
            initialize_session(result.get("user"))
            return redirect(url_for("main.index"))
        else:
            flash(result.get("error"), "error")
    return render_template("sign_in.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not email or not username or not password:
            return flash_and_redirect("All fields are required.", "error", "main.register")

        if len(password) < 8:
            return flash_and_redirect(
                "Password must be at least 8 characters long.", "error", "main.register"
            )

        result = UserActions.create_user(username, email, password)
        if result.get("success"):
            initialize_session(result.get("user"))
            return flash_and_redirect(
                "User created successfully. Welcome to MerkkiMylly!",
                "success",
                "main.index",
            )
        else:
            print(result.get("sys_error"))
            return flash_and_redirect(result.get("error"), "error", "main.register")
    return render_template("register.html")


@main.route("/click", methods=["POST"])
def click():
    if not session["user_id"]:
        return jsonify({"error": "User not logged in"}), 401

    if handle_buffer_update():
        return jsonify(
            {
                "clicks": session["clicks"],
                "click_buffer": session["click_buffer"],
                "points": session["points"],
                "point_buffer": session["point_buffer"],
            }
        )
    else:
        return jsonify({"error": "Database update failed"}), 500


@main.route("/buy", methods=["POST"])
def buy():
    if "user_id" not in session:
        return flash_and_redirect("User not signed in.")

    upgrade_id = request.form.get("upgrade_id")
    if not upgrade_id:
        return flash_and_redirect("Failed to get upgrade ID.")

    total_points = session.get("points", 0) + session.get("point_buffer", 0)

    result = UserActions.buy_upgrade(session["user_id"], upgrade_id, total_points)
    if result.get("success"):
        session["points"] = result["remaining_points"]
        session["point_buffer"] = 0
        session["click_power"] += result["upgrade_click_power"]
        session["passive_power"] += result["upgrade_passive_power"]

        for upgrade in session["user_upgrades"]:
            if upgrade["upgrade_id"] == result["upgrade_id"]:
                upgrade["amount"] = result["upgrade_amount"]

        flash(f"Successfully purchased {result['upgrade_name']}!", "success")
    else:
        flash(f"Failed to purchase upgrade: {result.get('error')}", "error")

    return redirect(url_for("main.index"))


@main.route("/save_game", methods=["POST"])
def save_game():
    if "user_id" not in session:
        return flash_and_redirect("User not signed in.")

    if session.get("click_buffer", 0) > 0:
        if handle_buffer_update(True):
            flash("Progress saved successfully.", "success")
        else:
            flash(
                "Something went wrong while saving your progress. Please try again.",
                "error",
            )
    else:
        flash("No new progress to save.", "info")

    return redirect(url_for("main.index"))


@main.route("/sign_out")
def sign_out():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.sign_in"))


@main.route("/profile")
def profile():
    return render_template("profile.html")
