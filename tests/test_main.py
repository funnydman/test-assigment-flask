import base64
import csv
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

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

dirpath = tempfile.mkdtemp()


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

    @patch("src.main.resources.FOLDER_TO_SAVE", dirpath)
    def test_upload_csv_file(self):
        content = b"first,second,third"
        content_encoded = base64.b64encode(content)
        data = {
            'file_content': content_encoded
        }
        res = self.app.post(f'{API_VERSION}/upload', data=data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['message'], 'File was decoded and saved')
        self.assertIsNotNone(os.listdir(dirpath)[0])
        self.assertTrue(os.listdir(dirpath)[0].endswith('.csv'))

        with open(dirpath + '/' + os.listdir(dirpath)[0]) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            res = list(reader)[0]

        self.assertEqual(res, content.decode().split(','))
        shutil.rmtree(dirpath)

    def test_get_countries_population(self):
        actual_data = [{
            'name': 'Afghanistan', 'capital': 'Kabul', 'subregion': 'coverage report -n Asia',
            'population': 27657145}]
        expected_data = {
            'Afghanistan': 27657145
        }
        with requests_mock.Mocker() as m:
            m.get('https://restcountries.eu/rest/v2/all', json=actual_data)

            res = self.app.get(f'{API_VERSION}/countries/population',
                               headers={'Authorization': 'Bearer ' + self.get_token()})

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
            res = self.app.get(f'{API_VERSION}/countries/csv', headers={'Authorization': 'Bearer ' + self.get_token()})
        actual_result = res.data.decode()
        expected_result = 'name,capital,region,lat,long,population,alpha3Code\r\nAfghanistan,Kabul,Asia,33,65,27657145,ASM\r\n'
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.decode(), expected_result)

    def test_countries_pdf(self):
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
            res = self.app.get(f'{API_VERSION}/countries/pdf', headers={'Authorization': 'Bearer ' + self.get_token()})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-type'], 'application/pdf')
        self.assertEqual(res.headers['Content-Disposition'], 'attachment; filename=countries.pdf')
