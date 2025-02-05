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

        groups = [models.Group(name='British Heart Foundation',
                               description='Your donations are hugely '
                                           'appreciated and help us fund '
                                           'life saving research. Please '
                                           'donate via the handy donation '
                                           'drop point in store.',
                               address='Guiness Trust, King\'s Road',
                               city='London',
                               county='Greater London',
                               postcode='SW10 0TT',
                               email='info@bhf.org.uk'),
                  models.Group(name='Trussel Trust Leeds',
                               description='Your foodbank relies on your '
                                          'goodwill and support.',
                               address='Unit 3, Burley Hill',
                               city='Leeds',
                               county='West Yorkshire',
                               postcode='LS4 2PU',
                               email='info@foodbank.or.uk'),
                  models.Group(name='Leeds Community Centre',
                               description='Our mission is to provide a hub '
                                           'for the whole community to take '
                                           'part in a range of positive '
                                           'activities.',
                               address='48 Bilton Lane',
                               city='Leeds',
                               county='West Yorkshire',
                               postcode='LS1 3DD',
                               email='info@community.org.uk')]

        categories = [models.Category(name='Books'),
                      models.Category(name='Clothes'),
                      models.Category(name='Food'),
                      models.Category(name='Stationary')]

        items = [models.Item(name='Fiction', category_id=1),
                 models.Item(name='Non-Fiction', category_id=1),
                 models.Item(name='Wooly Jumpers', category_id=2),
                 models.Item(name='Tinned Fruit', category_id=3),
                 models.Item(name='UHT Milk', category_id=3),
                 models.Item(name='Dried Rice', category_id=3),
                 models.Item(name='Craft Materials', category_id=4),
                 models.Item(name='Whiteboard Pens', category_id=4),]

        items_requested = [models.ItemRequested(item_id=1, group_id=1),
                           models.ItemRequested(item_id=2, group_id=1),
                           models.ItemRequested(item_id=3, group_id=1),
                           models.ItemRequested(item_id=4, group_id=2),
                           models.ItemRequested(item_id=5, group_id=2),
                           models.ItemRequested(item_id=6, group_id=2),
                           models.ItemRequested(item_id=7, group_id=3),
                           models.ItemRequested(item_id=2, group_id=3),]


        db.session.add_all(groups)
        db.session.add_all(categories)
        db.session.add_all(items)
        db.session.add_all(items_requested)
        db.session.commit()

    return app

