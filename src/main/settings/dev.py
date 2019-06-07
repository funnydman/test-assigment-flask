from sqlalchemy.engine.url import URL

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
TESTING = True
SECRET_KEY = 'dev'

DATABASE_USER = 'selena'
DATABASE_PASSWORD = 'selena'
DATABASE_NAME = 'mydatabase'
DATABASE_HOST = 'localhost'
DATABASE_POST = 5432

JWT_SECRET_KEY = 'jwt-secret-string'
JWT_TOKEN_LOCATION = 'cookies'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ('access', 'refresh')

DATABASE = {'drivername': 'postgres',
            'database': DATABASE_NAME,
            'username': DATABASE_USER,
            'password': DATABASE_PASSWORD,
            'host': DATABASE_HOST,
            'port': DATABASE_POST}

SQLALCHEMY_DATABASE_URI = URL(**DATABASE)
