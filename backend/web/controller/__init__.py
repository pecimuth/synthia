from flask import Flask

from web.controller.data_source import source
from web.controller.column import column
from web.controller.generator import generator
from web.controller.table import table
from web.controller.auth import auth
from web.controller.project import project
from web.service.json_encoder import JsonEncoder


def init_app(app: Flask):
    """Register all blueprints."""
    app.json_encoder = JsonEncoder
    app.register_blueprint(auth)
    app.register_blueprint(project)
    app.register_blueprint(table)
    app.register_blueprint(generator)
    app.register_blueprint(column)
    app.register_blueprint(source)
