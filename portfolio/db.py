import click
from flask import current_app, g
from flask.cli import with_appcontext
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list

from portfolio.models import db_wrapper, User, Post

def init_app(app):
    db_wrapper.init_app(app)
    app.cli.add_command(init_db_command)

def init_db():
    db = db_wrapper.database
    db.connect()
    db.create_tables([User, Post])

# This decorator makes the below function into a CLI command
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')