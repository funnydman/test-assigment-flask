import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(BASE_DIR)

app = Flask(__name__)

api = Api(app)

app.config.from_pyfile('main/settings/dev.py')
app.config.from_pyfile('main/settings/prod.py', silent=True)

db = SQLAlchemy(app)

jwt = JWTManager(app)
