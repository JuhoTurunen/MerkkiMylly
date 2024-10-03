from os import getenv

class Config:
    CLICK_THRESHOLD = 10
    PRICE_GROWTH_FACTOR = 1.15
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
