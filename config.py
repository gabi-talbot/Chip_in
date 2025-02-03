import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    FLASK_ENV = 'development'



class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    FLASK_ENV = 'testing'
    TESTING = True
    DEBUG = True

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}