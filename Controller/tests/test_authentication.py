from ..factory import create_app

import sys
sys.path.append('../..')
from mplib.model import util, model
from mplib.auth import authentication

from unittest import TestCase

class TestAuthenticationController (TestCase):

    @classmethod
    def setUpClass (self):
        self.redis = 'redis://127.0.0.1:6379'
        self.db = 'postgresql://test:test@localhost/mpdb'
        self.expiry = 500


    def setUp (self):
        self.app = create_app() # Build plain flask app
        self.app.config['SECRET_KEY'] = 'super_secret_secret'
        self.app.config['SERVICE_TYPE_FOR_AUTH'] = 'GAME'
        self.app.config['CELERY_RESULT_BACKEND'] = self.redis
        self.app.config['CELERY_BROKER_URL'] = self.redis
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        with self.app.app_context():
            util.drop_all()
            util.create_all()

            with util.transaction() as session:
                salt = authentication._generate_salt()
                player = model.DBPlayer (
                    username='markn',
                    first_name='Mark',
                    last_name='Nazzaro',
                    email='marknazzaro2@gmail.com',
                    pass_hash=authentication._get_pass_hash('passw0rD!', salt),
                    salt=salt,
                    account_balance=200
                )
                session.add(player)
                session.commit()
    
    def tearDown (self):
        with self.app.app_context():
            util.drop_all()

            with util.transaction() as session:
                session.commit()

    def test_login_success (self):
        with self.app.app_context():
            with self.client as client:
                response = client.post('/login', json={
                    'email': 'marknazzaro2@gmail.com',
                    'password': 'passw0rD!'
                })
        self.assertEqual(response.status_code, 200, "Response status was not 200")
        self.assertEqual(response.json['result'], True, "JSON result was not True")

    def test_login_wrong_pass (self):
        with self.app.app_context():
            with self.client as client:
                response = client.post('/login', json={
                    'email': 'marknazzaro2@gmail.com',
                    'password': 'wrong_password'
                })
        self.assertEqual(response.status_code, 403, "Response status was not 403")
        self.assertEqual(response.json['result'], False, "JSON result was not False")

    def test_login_unmatched_email (self):
        with self.app.app_context():
            with self.client as client:
                response = client.post('/login', json={
                    'email': 'badguy@gmail.com',
                    'password': 'evil_password'
                })
        self.assertEqual(response.status_code, 403, "Response status was not 403")
        self.assertEqual(response.json['result'], False, "JSON result was not False")