import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_dict
from flask_migrate import Migrate

from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()
# migrate = Migrate()

def create_app(config):

    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:abc@127.0.0.1:5432/chipin"
    app.config.from_object(config)
    # config[config_name].init_app(app)
    # app.config.from_pyfile("../config.py")


    # initialise database
    db.init_app(app)


    # For all endpoints
    CORS(app)

    # after a request is received this method is run. Sets CORS headers on the response.
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS')
        return response
    # allow models to be accessed
    from backend import models

    # register bluprint to access endpoints
    from backend.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Flask cli command to seed the database
    @app.cli.command('initdb')
    def initdb_command():

        groups = [models.Group(name='initdb', description='Initialize the database.',
                      address='postgres',
                      city='test',
                      county='test',
                      email='<EMAIL>'),

                 models.Group(name='Trussel Trust', description='Your local food bank.',
                              address='Trussel Trust',
                              city='Leeds',
                              county='North Yorkshire',
                              email='<EMAIL>')]

        categories = [models.Category(name='Books', slug='Books', image_link='to-do'),
                    models.Category(name='Clothes', slug='clothes', image_link='to-do'),
                    models.Category(name='Food', slug='food', image_link='to-do')]

        items = [models.Item(name='Fiction', description='Any fiction books please', category_id=1),
                models.Item(name='Children\'s tops', description='Summer tops, all ages needed', category_id=2),
                models.Item(name='Fruit', description='Fresh fruit in high demand', category_id=3)]

        items_requested = [models.ItemRequested(item_id=1, group_id=1), models.ItemRequested(item_id=2, group_id=2),
                           models.ItemRequested(item_id=3, group_id=1)]


        db.session.add_all(groups)
        db.session.add_all(categories)
        db.session.add_all(items)
        db.session.add_all(items_requested)
        db.session.commit()
        db.session.close()

    return app

