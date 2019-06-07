import click
from flask.cli import with_appcontext

from src.app import db


@click.command()
@with_appcontext
def drop_db():
    """Drop database tables."""
    db.drop_all()
