import os
import unittest
import config
from src.app import app, db
import json

TEST_DB = 'test.db'


class UserControllerTests(unittest.TestCase):
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

    ###############
    #### tests ####
    ###############

    def test_signup(self):
        response = self.signup("hitesh_sethi", "temp123")
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully added', response.data)

    def test_failed_validation_signup(self):
        response = self.signup("", "")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed validating', response.data)


if __name__ == "__main__":
    unittest.main()
