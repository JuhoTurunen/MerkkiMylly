from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash
from ..database import db


def create_user(username, email, password):
    try:
        existing_user = db.session.execute(
            text("SELECT * FROM users WHERE LOWER(username) = :username OR LOWER(email) = :email"),
            {"username": username.lower(), "email": email.lower()},
        ).fetchone()

        if existing_user:
            return {"error": "Failed to create user: Username or email already exists."}

        result = db.session.execute(
            text(
                """
                INSERT INTO users (username, email, password_hash) 
                VALUES (:username, :email, :password_hash) 
                RETURNING *
                """
            ),
            {
                "username": username,
                "email": email,
                "password_hash": generate_password_hash(password),
            },
        )
        db.session.flush()

        user = result.fetchone()
        user_id = user.id
        db.session.execute(
            text("INSERT INTO user_score (user_id) VALUES (:user_id)"), {"user_id": user_id}
        )

        db.session.commit()
        return {"success": True, "user": user}
    except Exception as e:
        db.session.rollback()
        return {
            "error": "An unexpected error occurred.",
            "syserror": str(e),
        }


def delete_user(user_id):
    try:
        result = db.session.execute(
            text("DELETE FROM users WHERE user_id = :user_id"),
            {"user_id": user_id},
        )
        if result.rowcount != 1:
            raise Exception(f"Expected to alter one row. Instead affected {result.rowcount}")
        db.session.commit()
        return {"success": True}
    except Exception as e:
        db.session.rollback()
        return {
            "syserror": e,
            "error": "Failed to delete account. Please try again later or reach out to game support.",
        }



def update_user_data(user_id, **kwargs):
    try:
        for key, value in kwargs.items():
            table = key.split(".", 1)[0]
            table_key = key.split(".", 1)[1]
            result = db.session.execute(
                text(f"UPDATE {table} SET {table_key} = :value WHERE user_id = :user_id"),
                {"value": value, "user_id": user_id},
            )
            if result.rowcount == 0:
                raise NoResultFound(f"Update for {key} failed.")

        db.session.commit()
        return {"success": True}
    except Exception as e:
        db.session.rollback()
        return {"syserror": str(e)}


def check_password(username, password):
    try:
        user = db.session.execute(
            text("SELECT * FROM users WHERE LOWER(username) = LOWER(:username)"),
            {"username": username},
        ).fetchone()

        if user and check_password_hash(user.password_hash, password):
            return {"success": True, "user": user}
        return {"error": "Wrong password or username."}
    except Exception as e:
        return {"syserror": str(e)}
