import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgres://localhost/flask-heroku'

class ProductionConfig(Config):
    DATABASE_URI = os.environ.get("DATABASE_URI")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True