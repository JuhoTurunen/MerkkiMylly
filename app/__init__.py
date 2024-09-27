from flask import Flask
from dotenv import load_dotenv
from .config import DevelopmentConfig
from .database import db
from .routes import main

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.secret_key = app.config["SECRET_KEY"]

    app.register_blueprint(main)

    return app
