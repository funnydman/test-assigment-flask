import os

from sqlalchemy.engine.url import URL

DEBUG = True
TESTING = True

SECRET_KEY = 'test'

SQLALCHEMY_TRACK_MODIFICATIONS = False

PROJECT_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
))

TEST_FOLDER_PATH = os.path.join(PROJECT_DIR, 'tests')

DATABASE = {
    'drivername': 'sqlite',
    'database': ':memory:'
}

SQLALCHEMY_DATABASE_URI = URL(**DATABASE)
