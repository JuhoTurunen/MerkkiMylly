from datetime import datetime, timezone, timedelta
import secrets
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

from .user_actions import *

main = Blueprint("main", __name__)


def initialize_session(user):
    session.clear()
    session["user_id"] = user.id
    session["username"] = user.username
    session["email"] = user.email

    session_end = get_session_end(user.id)

    if not session_end.get("success"):
        print(session_end.get("syserror"))

    session["last_cps_update"] = session_end.get("session_end")

    user_score = get_user_score(user.id)
    if user_score.get("success"):
        user_score = user_score["user_score"]
        session["clicks"] = user_score["clicks"]
        session["points"] = user_score["points"]
    else:
        print(user_score.get("syserror"))
        flash(user_score.get("error", "Failed to load score data. Please try again."), "error")

    user_game_data = get_user_game_data(user.id)
    if user_game_data.get("success"):
        session["user_upgrades"] = user_game_data["upgrades"]
        session["click_power"] = user_game_data["click_power"]
        session["passive_power"] = user_game_data["passive_power"]
    else:
        print(user_game_data.get("syserror"))
        flash(user_game_data.get("error", "Failed to load game data. Please try again."), "error")


def flash_and_redirect(message, category="error", route="main.index"):
    flash(message, category)
    return redirect(url_for(route))


def create_csrf_token():
    if not session.get("csrf"):
        session["csrf"] = secrets.token_hex(16)


def check_csrf_token(token, redirect_to):
    if session.get("csrf") != token or token is None:
        print(f"csrf Error. Token is {session.get('csrf')}, received {token}")
        return flash_and_redirect("Invalid request. Please try again later.", "error", redirect_to)


def round_to_nearest(number, nearest=5):
    return nearest * round(number / nearest)


def calculate_price(base_price, current_amount, buy_amount=1):
    total_price = 0
    for i in range(buy_amount):
        amount = current_amount + i
        total_price += round_to_nearest(
            base_price * (current_app.config["PRICE_GROWTH_FACTOR"] ** amount)
        )
    return total_price


def handle_cps():
    current_time = datetime.now(timezone.utc)

    last_cps_update = session["last_cps_update"].astimezone(timezone.utc)

    time_difference = (current_time - last_cps_update).total_seconds()

    full_seconds, fractional_seconds = divmod(time_difference, 1)

    leftover_time = timedelta(seconds=fractional_seconds)

    passive_power = session.get("passive_power", 0)
    passive_points = passive_power * int(full_seconds)

    session["points"] += passive_points

    session["last_cps_update"] = current_time - leftover_time
    update_session(session["user_id"], session["last_cps_update"])


def update_score(enable_threshold=False):
    if enable_threshold:
        check_csrf_token(request.headers.get("csrf"), "main.index")
        session["click_buffer"] = session.get("click_buffer", 0) + 1
        session["point_buffer"] = session.get("point_buffer", 0) + session.get("click_power", 1)

    if not enable_threshold or session["click_buffer"] >= current_app.config["CLICK_THRESHOLD"]:
        session["click_buffer"] = session.get("click_buffer", 0)
        session["point_buffer"] = session.get("point_buffer", 0)

        old_points = session["points"]

        session["points"] += session["point_buffer"]
        handle_cps()

        if old_points == session["points"]:
            return {"error": "Nothing to update"}

        session["clicks"] += session["click_buffer"]
        result = update_user_data(
            session["user_id"],
            **{
                "user_score.clicks": session["clicks"],
                "user_score.points": session["points"],
            },
        )
        if result.get("success"):
            session["click_buffer"] = 0
            session["point_buffer"] = 0
        else:
            print(result.get("syserror"))
            return {"error": result.get("error", "Failed to update database. Try again later.")}
    return {"success": True}


@main.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html")

    update_score()

    create_csrf_token()

    game_data = {
        "username": session["username"],
        "clicks": session.get("clicks", 0) + session.get("click_buffer", 0),
        "points": session.get("points", 0) + session.get("point_buffer", 0),
        "click_power": session.get("click_power", 1),
        "passive_power": session.get("passive_power", 0),
        "leaderboard": [],
    }

    leaderboard_result = get_leaderboard()
    if leaderboard_result.get("success"):
        game_data["leaderboard"] = leaderboard_result["leaderboard"]
    else:
        print(leaderboard_result.get("syserror"))

    session["upgrades"] = []
    upgrade_data = []

    upgrades_result = list_upgrades()
    if upgrades_result.get("success"):
        upgrades = upgrades_result["upgrades"]

        upgrade_amounts = {u["upgrade_id"]: u["amount"] for u in session.get("user_upgrades", [])}

        for upgrade in upgrades:

            user_upgrade_amount = upgrade_amounts.get(upgrade["id"], 0)

            price = session.get(
                "price", calculate_price(upgrade["base_price"], user_upgrade_amount)
            )

            session["upgrades"].append(
                {
                    "id": upgrade["id"],
                    "click_power": upgrade["click_power"],
                    "passive_power": upgrade["passive_power"],
                    "base_price": upgrade["base_price"],
                    "price": price,
                }
            )

            buff = (
                f"Bonus click power: {upgrade['click_power']}"
                if upgrade["click_power"] != 0
                else f"CPS bonus: {upgrade['passive_power']}"
            )

            upgrade_data.append(
                {
                    "upgrade_id": upgrade["id"],
                    "name": upgrade["name"],
                    "buff": buff,
                    "base_price": upgrade["base_price"],
                    "price": price,
                    "description": upgrade["description"],
                    "amount": user_upgrade_amount,
                }
            )
        upgrade_data = sorted(upgrade_data, key=lambda x: x["base_price"])
    else:
        print(upgrades_result.get("syserror"))
        flash(upgrades_result.get("error", "Could not get upgrades. Try again later."), "error")

    return render_template(
        "game.html", game_data=game_data, upgrades=upgrade_data, csrf=session["csrf"]
    )


@main.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        create_csrf_token()
        return render_template("sign_in.html", csrf=session["csrf"])
    if request.method == "POST":
        check_csrf_token(request.form.get("csrf"), "main.sign_in")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        result = check_password(username, password)
        if result.get("success"):
            initialize_session(result.get("user"))
            old_points = session["points"]
            update_score()
            gained_points = session["points"] - old_points
            return flash_and_redirect(
                f"You've collected {gained_points} points from offline gains!", "success"
            )
        print(result.get("syserror"))
        flash(result.get("error", "Failed to sign in. Please try again later."), "error")
        return render_template("sign_in.html", username=username, csrf=session["csrf"])


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        create_csrf_token()
        return render_template("register.html", csrf=session["csrf"])
    if request.method == "POST":
        check_csrf_token(request.form.get("csrf"), "main.register")
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        form_data = {"email": email, "username": username}

        if not email or not username or not password:
            flash("All fields are required.", "error")
            return render_template("register.html", form_data=form_data, csrf=session["csrf"])

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return render_template("register.html", form_data=form_data, csrf=session["csrf"])

        result = create_user(username, email, password)
        if result.get("success"):
            initialize_session(result.get("user"))
            return flash_and_redirect(
                "User created successfully. Welcome to MerkkiMylly!",
                "success",
            )
        print(result.get("syserror"))
        flash(result.get("error", "Failed to create account. Please try again later."), "error")
        return render_template("register.html", form_data=form_data, csrf=session["csrf"])


@main.route("/click", methods=["POST"])
def click():
    if not session["user_id"]:
        return jsonify({"error": "User not signed in."})
    result = update_score(True)
    if result.get("success"):
        return jsonify(
            {
                "clicks": session["clicks"],
                "click_buffer": session["click_buffer"],
                "points": session["points"],
                "point_buffer": session["point_buffer"],
            }
        )
    return jsonify({"error": "Failed to update clicks to server. Please try again later."})


@main.route("/buy", methods=["POST"])
def buy():
    check_csrf_token(request.headers.get("csrf"), "main.index")
    if "user_id" not in session:
        return jsonify({"error": "User not signed in."})

    upgrade_id = request.form.get("upgrade_id")
    if not upgrade_id:
        return jsonify({"error": "Failed to get upgrade ID."})

    try:
        buy_amount = int(request.form.get("buy_amount", 1))
        if buy_amount < 1 or buy_amount > 99:
            return jsonify({"error": "Buy amount needs to be a number from 1 to 99."})
    except ValueError:
        return jsonify({"error": "Invalid buy amount."})

    upgrade = next(
        (u for u in session.get("upgrades", []) if str(u["id"]) == str(upgrade_id)), None
    )

    if not upgrade:
        return jsonify({"error": "Could not verify upgrade. Please try again later."})

    total_points = session.get("points", 0) + session.get("point_buffer", 0)

    user_upgrade = next(
        (uu for uu in session["user_upgrades"] if uu["upgrade_id"] == upgrade["id"]), None
    )

    current_amount = user_upgrade["amount"] if user_upgrade else 0

    price = calculate_price(upgrade["base_price"], current_amount, buy_amount)

    remaining_points = total_points - price
    if remaining_points < 0:
        return jsonify({"error": "Not enough points to buy this upgrade."})

    result = buy_upgrade(session["user_id"], upgrade["id"], buy_amount)

    if not result.get("success"):
        print(result.get("syserror"))
        return jsonify({"error": "Failed to purchase upgrade. Please try again later."})

    session["points"] = remaining_points
    session["point_buffer"] = 0
    session["click_power"] += upgrade["click_power"] * buy_amount
    session["passive_power"] += upgrade["passive_power"] * buy_amount
    upgrade["price"] = calculate_price(upgrade["base_price"], (current_amount + buy_amount))

    if user_upgrade:
        user_upgrade["amount"] += buy_amount
    else:
        session["user_upgrades"].append(
            {
                "upgrade_id": upgrade["id"],
                "amount": buy_amount,
                "click_power": upgrade["click_power"],
                "passive_power": upgrade["passive_power"],
            }
        )

    return jsonify(
        {
            "upgrade_id": upgrade_id,
            "buy_amount": buy_amount,
            "price": upgrade["price"],
            "remaining_points": remaining_points,
            "passive_power": session["passive_power"],
        }
    )


@main.route("/save_game", methods=["POST"])
def save_game():
    check_csrf_token(request.form.get("csrf"), "main.index")
    if "user_id" not in session:
        return flash_and_redirect("User not signed in.")

    result = update_score()
    if result.get("success"):
        flash("Progress saved successfully.", "success")
    else:
        flash(
            result.get(
                "error",
                "Something went wrong while saving your progress. Please try again later.",
            ),
            "error",
        )

    return redirect(url_for("main.index"))


@main.route("/sign_out")
def sign_out():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.sign_in"))


@main.route("/profile")
def profile():
    search_username = request.args.get("username") or session["username"]
    result = get_profiles(search_username)
    if result.get("success"):
        profiles = result["user_profile"]
        if profiles[0]["username"].lower() == search_username.lower():
            profiles = profiles[0]
        if search_username.lower() == session["username"].lower():
            profiles.update({"owner": True, "email": session["email"]})

    else:
        print(result.get("syserror"))
        return flash_and_redirect(
            result.get("error", "Failed to get profile data. Please try again later."),
            "error",
            "main.profile",
        )
    return render_template("profile.html", profiles=profiles)
