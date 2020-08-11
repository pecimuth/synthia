from flask import Blueprint, Flask
from app.controller.schema import schema

def init_app(app: Flask):
    app.register_blueprint(schema)
