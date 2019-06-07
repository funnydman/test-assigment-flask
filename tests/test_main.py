import base64
import unittest

from src.app import app
from src.app import db
from src.run import API_VERSION
from src.users.models import User
from tests import utils

TEST_USER = {
    'username': 'selena',
    'password': 'gomez',
    'name': 'Selena',
    'surname': 'Gomez',
    'email': 'selena@gomezz.ru'
}


class TestUsersModels(unittest.TestCase):
    def setUp(self):
        utils.init_test_database()
        self.app = app.test_client()
        self.app.testing = True
        self.new_user = User(
            username=TEST_USER['username'],
            password=User.generate_hash(TEST_USER['password']),
            name=TEST_USER['name'],
            surname=TEST_USER['surname'],
            email=TEST_USER['email']
        )
        self.new_user.save_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_upload_csv_file(self):
        content = b"first,second,third"
        content_encoded = base64.b64encode(content)
        data = {
            'file_content': content_encoded
        }
        res = self.app.post(f'{API_VERSION}/upload', data=data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['message'], 'File was decoded and saved')
