from flask import current_app, g, Flask
from flask.cli import with_appcontext
from app import model
from app.service.database import get_db_engine, close_db
import click

@click.command('create-db')
@with_appcontext
def create_db_command():
    model.base.metadata.create_all(get_db_engine())
    click.echo('Created the database')

def init_app(app: Flask):
    app.cli.add_command(create_db_command)
    app.teardown_appcontext(close_db)
