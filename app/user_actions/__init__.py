from sqlalchemy import text
from ..database import db

def update_session(user_id):
    result = db.session.execute(
        text(
            """
            UPDATE user_session SET last_update_timestamp = CURRENT_TIMESTAMP 
            WHERE user_id = :user_id
            """
        ),
        {"user_id": user_id},
    )
    if result.rowcount == 0:
        db.session.execute(
            text(
                """
                INSERT INTO user_session (user_id, last_update_timestamp)
                VALUES (:user_id, CURRENT_TIMESTAMP)
                """
            ),
            {"user_id": user_id},
        )
    db.session.commit()
