from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash
from .database import db
from .models import User, ScoreData, Upgrade, UserUpgrade


class UserActions:
    @staticmethod
    def create_user(username, email, password):
        existing_user = User.query.filter(
            (func.lower(User.username) == func.lower(username))
            | (func.lower(User.email) == func.lower(email))
        ).first()

        if existing_user:
            return {"error": "Failed to create user: Username or email already exists."}

        try:
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
            )
            db.session.add(new_user)
            db.session.commit()

            new_user.score_data = ScoreData()

            db.session.add(new_user)
            db.session.commit()
            return {"success": True, "user": new_user}
        except Exception as e:
            db.session.rollback()
            return {
                "error": "An unexpected error occurred.",
                "sys_error": e,
            }

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {"success": True}
            return {"error": "User not found."}
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete user: {e}"}

    @staticmethod
    def update_user(user_id, **kwargs):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found."}
            for key, value in kwargs.items():
                if key.startswith("score_data."):
                    score_data_attr = key.split(".", 1)[1]
                    if hasattr(user.score_data, score_data_attr):
                        setattr(user.score_data, score_data_attr, value)
                else:
                    setattr(user, key, value)
            db.session.commit()
            return {"success": True, "user": user}
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update user: {e}"}

    @staticmethod
    def check_password(username, password):
        try:
            user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
            if user and check_password_hash(user.password_hash, password):
                return {"success": True, "user": user}
            return {"error": "Wrong password or username."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

    @staticmethod
    def buy_upgrade(user_id, upgrade_id, total_points):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found."}

            upgrade = Upgrade.query.get(upgrade_id)
            if not upgrade:
                return {"error": "Upgrade not found."}

            score_data = user.score_data
            if not score_data:
                return {"error": "User score data not found."}

            if total_points < upgrade.price:
                return {"error": "Not enough points to buy this upgrade."}

            try:
                user_upgrade = UserUpgrade.query.filter_by(
                    user_id=user.id, upgrade_id=upgrade.id
                ).one()
                user_upgrade.amount += 1
            except NoResultFound:
                user_upgrade = UserUpgrade(user_id=user.id, upgrade_id=upgrade.id, amount=1)
                db.session.add(user_upgrade)

            score_data.points = total_points - upgrade.price

            db.session.commit()

            return {
                "success": True,
                "upgrade_id": upgrade.id,
                "upgrade_name": upgrade.name,
                "upgrade_amount": user_upgrade.amount,
                "remaining_points": score_data.points,
                "upgrade_click_power": upgrade.click_power,
                "upgrade_passive_power": upgrade.passive_power,
            }
        except IntegrityError as e:
            db.session.rollback()
            return {"error": f"Database integrity error occurred: {e}"}
        except Exception as e:
            db.session.rollback()
            return {"error": f"An unexpected error occurred: {e}"}

    @staticmethod
    def get_user_game_data(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"error": "User not found."}

            user_upgrades = (
                db.session.query(UserUpgrade, Upgrade)
                .join(Upgrade)
                .filter(UserUpgrade.user_id == user.id)
                .all()
            )

            upgrades = [
                {
                    "upgrade_id": upgrade.id,
                    "amount": user_upgrade.amount,
                    "click_power": upgrade.click_power,
                    "passive_power": upgrade.passive_power,
                }
                for user_upgrade, upgrade in user_upgrades
            ]

            click_power = (
                sum(upgrade["click_power"] * upgrade["amount"] for upgrade in upgrades) + 1
            )
            passive_power = sum(
                upgrade["passive_power"] * upgrade["amount"] for upgrade in upgrades
            )

            return {
                "success": True,
                "upgrades": upgrades,
                "click_power": click_power,
                "passive_power": passive_power,
            }
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

    @staticmethod
    def list_upgrades():
        try:
            return {"success": True, "upgrades": Upgrade.query.all()}
        except Exception as e:
            return {"error": f"Failed to fetch upgrades: {e}"}
