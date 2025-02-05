import json
import unittest

from flask import request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from backend import create_app, db
from backend.models import Group, Category, Item, ItemRequested
from config import config_dict, Config, TestingConfig, DevelopmentConfig


class GroupTestCase(unittest.TestCase):
    """Testing the Group resource"""


    def setUp(self):
        """Initialise the app and create test variables"""
        self.header = {"Authorization": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6Ik'
                                        'pXVCIsImtpZCI6Ii1nejJXN2h0S1d6bjY0Mm1'
                                        'KRjBZeiJ9.eyJpc3MiOiJodHRwczovL2NoaXB'
                                        'pbi1hdXRoLnVrLmF1dGgwLmNvbS8iLCJzdWIi'
                                        'OiJhdXRoMHw2Nzk3NjM0Yjc4MmNjYmY0ZGQ2Zj'
                                        'cwMTAiLCJhdWQiOiJjaGlwaW4iLCJpYXQiOjE3'
                                        'Mzg3NjQ2MzEsImV4cCI6MTczODg1MTAzMSwic'
                                        '2NvcGUiOiIiLCJhenAiOiJqMnE2OU5MRTl4dU'
                                        'w5NHcwdzVrWlhNWk1KU1J4MEs2YSIsInBlcm1'
                                        'pc3Npb25zIjpbImRlbGV0ZTppdGVtX3JlcXVl'
                                        'c3RlZCIsInBhdGNoOmdyb3VwX2VtYWlsIiwic'
                                        'G9zdDpncm91cCIsInBvc3Q6aXRlbV9yZXF1ZX'
                                        'N0ZWQiXX0.m52o8CRb_k7cmhvOFKh7qZH-ikm'
                                        'M6kJIReBDZfxjECENJTO1EGsql-93pExiu6H0'
                                        '7Y3wtSXJcPuzwoGZ0lPV8w_47zWkkWPW3CZuu'
                                        'rvSoUl_QMj0GRyjqyZfV2bD_qM0ukQPlVBZQh'
                                        'EZiu96z_BE-cqnm-S3V25kobVlcK-NI0AiJkK'
                                        'i9aN7SCPtRZ-8zXzz2S5bUhBxJIw1xB_Wukq4'
                                        'hFFLs0bYAUCm5FCRwawJ6vKWFcuIUkvIjdkF6'
                                        'wBN2VaRNPQWgEqu5OjsLCsbvaj2JFcsnxq6P0'
                                        'hLI-tpl9eYT7fvx-ZsaWB4Tnoj-aPJnldaHy'
                                        'WJSX7pvyq7FlUcYWx3Dw'}

        self.app = create_app(TestingConfig)

        self.client = self.app.test_client

        with self.app.app_context():

            db.create_all()
            groups = [Group(name='British Heart Foundation',
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
                      Group(name='Trussel Trust Leeds',
                           description='Your foodbank relies on your '
                                       'goodwill and support.',
                           address='Unit 3, Burley Hill',
                           city='Leeds',
                           county='West Yorkshire',
                           postcode='LS4 2PU',
                           email='info@foodbank.or.uk'),
                      Group(name='Leeds Community Centre',
                           description='Our mission is to provide a hub '
                                       'for the whole community to take '
                                       'part in a range of positive '
                                       'activities.',
                           address='48 Bilton Lane',
                           city='Leeds',
                           county='West Yorkshire',
                           postcode='LS1 3DD',
                           email='info@community.org.uk')]

            categories = [Category(name='Books'),
                          Category(name='Clothes'),
                          Category(name='Food'),
                          Category(name='Stationary')]

            items = [Item(name='Fiction', category_id=1),
                     Item(name='Non-Fiction', category_id=1),
                     Item(name='Wooly Jumpers', category_id=2),
                     Item(name='Tinned Fruit', category_id=3),
                     Item(name='UHT Milk', category_id=3),
                     Item(name='Dried Rice', category_id=3),
                     Item(name='Craft Materials', category_id=4),
                     Item(name='Whiteboard Pens', category_id=4)]

            items_requested = [ItemRequested(item_id=1, group_id=1),
                               ItemRequested(item_id=2, group_id=1),
                               ItemRequested(item_id=3, group_id=1),
                               ItemRequested(item_id=4, group_id=2),
                               ItemRequested(item_id=5, group_id=2),
                               ItemRequested(item_id=6, group_id=2),
                               ItemRequested(item_id=7, group_id=3),
                               ItemRequested(item_id=2, group_id=3)]

            db.session.add_all(groups)
            db.session.add_all(categories)
            db.session.add_all(items)
            db.session.add_all(items_requested)
            db.session.commit()

        self.new_group = Group(name="Test Group", description="Test description",
                               address="Test address", city="Test city",
                               county="Test county",
                               postcode= "SW1 2BB", email="test@email.com")


    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.drop_all()

################# GET endpoints #################################

    def test_get_paginated_groups(self):
        response = self.client().get('api/groups')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_groups'])

    def test_404_requesting_beyond_valid_page(self):
        response = self.client().get('api/groups?page=1000', json={"name":
                                                                      "hi"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Groups not found')

    def test_get_group_by_id(self):
        response = self.client().get('api/groups/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['group']['name'], 'British Heart Foundation')


    def test_get_group_by_wrong_id(self):
        response = self.client().get('api/groups/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Group not found')


################### PATCH endpoint ##############################

    def test_update_group(self):
        response = self.client().patch('api/groups/1',
                                       headers=self.header,
                                       json={"email":"patch@patched.org.uk"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    def test_update_group_with_empty_string(self):
        response = self.client().patch('api/groups/1',
                                       headers=self.header,
                                       json={"email":""})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Email address is required')

    def test_post_group(self):
        response = self.client().post("/api/groups", headers=self.header,
                                      json={"name": "test group",
                                            "description": "test description",
                                            "address": "test address",
                                            "city": "test city",
                                            "county": "test county",
                                            "postcode": "test postcode",
                                            "email": "test email"})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

if __name__ == '__main__':
    unittest.main()