from src.app import app
from src.app import db


def init_test_database():
    app.config.from_pyfile(f'main/settings/test.py')
    db.create_all()
