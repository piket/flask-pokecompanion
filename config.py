import os
import flask_wtf

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True