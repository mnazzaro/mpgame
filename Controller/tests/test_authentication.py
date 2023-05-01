from ..factory import create_app

import sys
sys.path.append('../..')
from mplib.model import models, util
from mplib.auth import authentication, passwords
from mplib.auth.tokens.tokens import unpack_token

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
        self.app.config['JWT_SECRET'] = 'other_secret'
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
                salt = passwords._generate_salt()
                player = models.DBPlayer (
                    username='markn',
                    first_name='Mark',
                    last_name='Nazzaro',
                    email='marknazzaro2@gmail.com',
                    pass_hash=passwords._get_pass_hash('passw0rD!', salt),
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
        self.assertEqual(response.status_code, 200, response.json['result'])
        self.assertEqual(response.json['result'], True, "JSON result was not True")

        session = unpack_token(response.headers.get('access_token', 'NO ACCESS TOKEN'), self.app.config['JWT_SECRET'])
        self.assertEqual(session.user.user_id, 1, "user_id in token is incorrect")

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