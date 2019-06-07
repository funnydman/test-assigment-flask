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
    'database': os.environ['POSTGRES_DB'],
    'username': os.environ['POSTGRES_USER'],
    'password': os.environ['POSTGRES_PASSWORD'],
    'host': os.environ['POSTGRES_HOST'],
    'port': int(os.environ['POSTGRES_PORT'])
}

SQLALCHEMY_DATABASE_URI = URL(**DATABASE)
