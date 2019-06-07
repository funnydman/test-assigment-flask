import os
from logging import getLogger

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

logger = getLogger()

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

app = Flask(__name__)

api = Api(app)
try:
    app.config.from_pyfile('main/settings/conf.py')
except Exception as e:
    logger.warning(f'Can\'t load config: {e}')

db = SQLAlchemy(app)

jwt = JWTManager(app)
