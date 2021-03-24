from flask import Flask
from flask.cli import with_appcontext
from core import model
from web.service.database import get_db_engine, close_db
import click

from web.service.injector import pop_injector


@click.command('recreate-database')
@with_appcontext
def recreate_database_command():
    """Drop all tables in a database a recreate them."""
    model.base.metadata.drop_all(get_db_engine())
    model.base.metadata.create_all(get_db_engine())
    click.echo('Recreated the database')


def init_app(app: Flask):
    """Init the flask app.

    Here we should add commands and define tear down context.
    """
    app.cli.add_command(recreate_database_command)
    app.teardown_appcontext(close_db)
    app.teardown_appcontext(pop_injector)
