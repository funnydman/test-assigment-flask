import unittest

from src.app import app, db
from src.run import API_VERSION
from src.users.models import User

TEST_USER = {
    'username': 'selena',
    'password': 'gomez',
    'name': 'Selena',
    'surname': 'Gomez',
    'email': 'selena@gomezz.ru'
}


def init_test_database():
    app.config.from_pyfile(f'main/settings/test.py')
    db.create_all()


class TestUsersModels(unittest.TestCase):
    def setUp(self):
        init_test_database()

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

    def test_user_data(self):
        self.assertEqual(TEST_USER['username'], self.new_user.username)
        self.assertTrue(User.verify_hash(TEST_USER['password'], self.new_user.password))
        self.assertEqual(TEST_USER['name'], self.new_user.name)
        self.assertEqual(TEST_USER['surname'], self.new_user.surname)
        self.assertEqual(TEST_USER['email'], self.new_user.email)

    def test_find_by_username(self):
        user = User.find_by_username(TEST_USER['username'])
        self.assertEqual(user.name, TEST_USER['name'])

    def test_find_by_email(self):
        user = User.find_by_email(TEST_USER['email'])
        self.assertEqual(self.new_user.email, TEST_USER['email'])

    def test_return_all(self):
        user = User.return_all()
        self.assertEqual(self.new_user.username, TEST_USER['username'])


class TestUsersApi(unittest.TestCase):
    def setUp(self):
        init_test_database()

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

    def test_signin(self):
        res = self.app.post(f'{API_VERSION}/signin', data={
            'username': TEST_USER['username'],
            'password': TEST_USER['password']
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['message'], 'Logged in as selena')
        self.assertIsNotNone(res.get_json()['access_token'])
        self.assertIsNotNone(res.get_json()['refresh_token'])

    def test_signup(self):
        data = {
            'username': 'test_username',
            'password': 'test_password',
            'name': 'test_name',
            'surname': 'test_surname',
            'email': 'test_email'
        }
        res = self.app.post(f'{API_VERSION}/signup', data=data)
        self.assertEqual(res.status_code, 201)

        self.assertEqual(res.get_json()['message'], 'User test_username was created')
        self.assertIsNotNone(res.get_json()['access_token'])
        self.assertIsNotNone(res.get_json()['refresh_token'])

        res = self.app.post(f'{API_VERSION}/signup', data=data)
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.get_json()['message'], 'User test_username already exists')


if __name__ == '__main__':
    unittest.main()
