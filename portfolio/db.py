import click
from flask.cli import with_appcontext

from portfolio.models import db_wrapper, User, Post


def init_app(app):
    db_wrapper.init_app(app)
    app.cli.add_command(init_db_command)


def init_db():
    with db_wrapper.database:
        db_wrapper.database.create_tables([User, Post])
    db_wrapper.database.close()


# This decorator makes the below function into a CLI command
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
