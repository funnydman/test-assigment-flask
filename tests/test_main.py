import base64
import unittest

import requests_mock

from src.app import app, db
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

    def get_token(self):
        data = {
            'username': TEST_USER['username'],
            'password': TEST_USER['password']
        }
        res = self.app.post(f'{API_VERSION}/signin', data=data)
        return res.get_json()['access_token']

    def test_upload_csv_file(self):
        # TODO: do not store file in the project!
        content = b"first,second,third"
        content_encoded = base64.b64encode(content)
        data = {
            'file_content': content_encoded
        }
        res = self.app.post(f'{API_VERSION}/upload', data=data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['message'], 'File was decoded and saved')

    def test_get_countries_population(self):
        actual_data = [{
            'name': 'Afghanistan', 'capital': 'Kabul', 'subregion': 'Southern Asia',
            'population': 27657145}]
        expected_data = {
            'Afghanistan': 27657145
        }
        with requests_mock.Mocker() as m:
            m.get('https://restcountries.eu/rest/v2/all', json=actual_data)

            res = self.app.get(f'{API_VERSION}/countries/population', headers={'access_token_cookie': self.get_token()})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), expected_data)

    def test_countries_csv(self):
        keys = ('name', 'capital', 'region', 'lat', 'long', 'population', 'alpha3Code')
        actual_data = [{
            "name": "Afghanistan",
            "capital": "Kabul",
            "region": "Asia",
            "subregion": "Southern Asia",
            "population": 27657145,
            "latlng": [
                33,
                65
            ],
            "alpha3Code": "ASM"
        }]

        with requests_mock.Mocker() as m:
            m.get('https://restcountries.eu/rest/v2/all', json=actual_data)
            res = self.app.get(f'{API_VERSION}/countries/csv', headers={'access_token_cookie': self.get_token()})
        actual_result = res.data.decode()
        expected_result = 'name,capital,region,lat,long,population,alpha3Code\r\nAfghanistan,Kabul,Asia,33,65,27657145,ASM\r\n'
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.decode(), expected_result)
