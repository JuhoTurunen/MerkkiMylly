from .database import db
from sqlalchemy.sql import func
from sqlalchemy import BigInteger


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    score_data = db.relationship("ScoreData", backref="user", uselist=False)
    user_upgrades = db.relationship("UserUpgrade", backref="user", lazy="dynamic")


class ScoreData(db.Model):
    __tablename__ = "score_data"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    clicks = db.Column(BigInteger, default=0)
    points = db.Column(BigInteger, default=0)


class Upgrade(db.Model):
    __tablename__ = "upgrades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    click_power = db.Column(db.Integer, nullable=False, default=0)
    passive_power = db.Column(db.Integer, nullable=False, default=0)

    user_upgrades = db.relationship("UserUpgrade", backref="upgrade", lazy="dynamic")


class UserUpgrade(db.Model):
    __tablename__ = "user_upgrades"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    upgrade_id = db.Column(
        db.Integer, db.ForeignKey("upgrades.id", ondelete="CASCADE"), nullable=False
    )
    amount = db.Column(db.Integer, nullable=False)
