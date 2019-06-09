import os
from logging import getLogger

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

logger = getLogger(__name__)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

app = Flask(__name__, template_folder=os.path.join(PROJECT_DIR, 'templates'))

api = Api(app)

app.config.from_pyfile('main/settings/conf.py')

db = SQLAlchemy(app)

jwt = JWTManager(app)
