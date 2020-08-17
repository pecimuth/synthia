from flask import Flask

from app.controller.column import column
from app.controller.generator import generator
from app.controller.table import table
from app.controller.auth import auth
from app.controller.project import project


def init_app(app: Flask):
    app.register_blueprint(auth)
    app.register_blueprint(project)
    app.register_blueprint(table)
    app.register_blueprint(generator)
    app.register_blueprint(column)
