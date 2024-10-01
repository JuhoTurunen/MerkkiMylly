from sqlalchemy import text
from ..database import db


def buy_upgrade(user_id, upgrade_id, increase):
    try:
        result = db.session.execute(
            text(
                """
                UPDATE user_upgrades 
                SET amount = amount + :increase 
                WHERE user_id = :user_id 
                AND upgrade_id = :upgrade_id
                """
            ),
            {"user_id": user_id, "upgrade_id": upgrade_id, "increase": increase},
        )

        if result.rowcount == 0:
            db.session.execute(
                text(
                    """
                    INSERT INTO user_upgrades (user_id, upgrade_id, amount) 
                    VALUES (:user_id, :upgrade_id, :amount)
                    """
                ),
                {"user_id": user_id, "upgrade_id": upgrade_id, "amount": increase},
            )

        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        return {"syserror": str(e)}


def get_user_game_data(user_id):
    try:
        user_upgrades = db.session.execute(
            text(
                """
                SELECT user_upgrades.amount, upgrades.id, upgrades.click_power, 
                upgrades.passive_power 
                FROM user_upgrades 
                INNER JOIN upgrades 
                ON user_upgrades.upgrade_id=upgrades.id
                WHERE user_id = :user_id 
                """
            ),
            {"user_id": user_id},
        ).fetchall()

        upgrades = [
            {
                "upgrade_id": u.id,
                "amount": u.amount,
                "click_power": u.click_power,
                "passive_power": u.passive_power,
            }
            for u in user_upgrades
        ]
        click_power = sum(upgrade.click_power * upgrade.amount for upgrade in user_upgrades) + 1
        passive_power = sum(upgrade.passive_power * upgrade.amount for upgrade in user_upgrades)

        return {
            "success": True,
            "upgrades": upgrades,
            "click_power": click_power,
            "passive_power": passive_power,
        }
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


def get_user_score(user_id):
    try:
        user_score = db.session.execute(
            text(
                """SELECT user_score.clicks, user_score.points 
                FROM user_score 
                WHERE user_id = :user_id 
                """
            ),
            {"user_id": user_id},
        ).fetchone()

        if not user_score:
            return {
                "syserror": "user_score was Null.",
                "error": "Failed to find user score records.",
            }

        user_score_dict = {"clicks": user_score.clicks, "points": user_score.points}

        return {"success": True, "user_score": user_score_dict}
    except Exception as e:
        return {"syserror": str(e)}


def list_upgrades():
    try:
        result = db.session.execute(text("SELECT * FROM upgrades")).fetchall()
        upgrades = [
            {
                "id": upgrade.id,
                "name": upgrade.name,
                "description": upgrade.description,
                "price": upgrade.price,
                "click_power": upgrade.click_power,
                "passive_power": upgrade.passive_power,
            }
            for upgrade in result
        ]
        return {"success": True, "upgrades": upgrades}
    except Exception as e:
        return {"syserror": e}
