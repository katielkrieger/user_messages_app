import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgres://localhost/07-sql-alchemy-2'

class ProductionConfig(Config):
    DATABASE_URI = os.environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True