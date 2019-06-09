import os

from sqlalchemy.engine.url import URL

SQLALCHEMY_TRACK_MODIFICATIONS = False

# generated with command
# python3 -c 'import uuid; print(uuid.uuid4().hex)'
SECRET_KEY = 'dev'

JWT_SECRET_KEY = 'jwt-secret-string'
JWT_TOKEN_LOCATION = 'cookies'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ('access', 'refresh')

DATABASE = {
    'drivername': 'postgres',
    'database': os.environ.get('POSTGRES_DB', 'devdb'),
    'username': os.environ.get('POSTGRES_USER', 'admindev'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'admindev'),
    'host': os.environ.get('POSTGRES_HOST', 'localhost'),
    'port': int(os.environ.get('POSTGRES_PORT', 5432))
}

SQLALCHEMY_DATABASE_URI = URL(**DATABASE)
