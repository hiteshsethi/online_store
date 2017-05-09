import os
import unittest
import config
from src.app import app, db
import json

TEST_DB = 'test.db'
from base64 import b64encode


class ProductControllerTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(config.BASE_DIR, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    def signup(self, user_name, password):
        return self.app.post(
            config.API_PREFIX_V1 + '/user/signup',
            data=json.dumps(dict(user_name=user_name, password=password)),
            content_type='application/json',
            follow_redirects=True
        )

    def get_headers(self):
        user_name = "hitesh_sethi"
        password = "test123"
        response = self.signup(user_name=user_name, password=password)
        self.assertEqual(200, response.status_code)
        return {
            "Authorization": 'Basic ' + b64encode("{0}:{1}".format(user_name, password))
        }

    def add_product(self, name, description, category_id, is_active, price, headers={}):
        return self.app.post(
            config.API_PREFIX_V1 + '/product/add',
            data=json.dumps(
                dict(name=name, description=description, category_id=category_id, is_active=is_active, price=price)),
            headers=headers, content_type="application/json",
            follow_redirects=True
        )

    ###############
    #### tests ####
    ###############

    def test_add_product(self):
        headers = self.get_headers()
        response = self.add_product("product1", "random desc", 1, True, 1000, headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully added', response.data)

    def test_failed_validating_add_product(self):
        headers = self.get_headers()
        response = self.add_product("p1", "random desc", 1, True, -1000, headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed validating', response.data)

    def test_authorisation_add_product(self):
        response = self.add_product("product1", "random desc", 1, True, 1000)
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
