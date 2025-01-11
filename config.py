import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}