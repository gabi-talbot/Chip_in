import json
import unittest

from flask import request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from backend import create_app, db
from backend.models import Group
from config import config_dict, Config, TestingConfig, DevelopmentConfig


class GroupTestCase(unittest.TestCase):
    """Testing the Group resource"""


    def setUp(self):
        """Initialise the app and create test variables"""

        self.app = create_app(DevelopmentConfig)

        self.client = self.app.test_client

        with self.app.app_context():

            db.create_all()

        self.new_group = Group(name="Test Group", description="Test description",
                               address="Test address", city="Test city",
                               county="Test county", email="<EMAIL>",
                               image_link="http://test.com")


    def tearDown(self):
        """Executed after each test"""
        pass

# I think the test is fine but not accessing the db, so len of groups == 0???
    # create a separate test_config file?
    def test_get_paginated_groups(self):
        response = self.client().get("/group")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])

    def test_404_requesting_beyond_valid_page(self):
        response = self.client().get("/group?page=1000", json={"name": "hi"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Not Found')


if __name__ == '__main__':
    unittest.main()