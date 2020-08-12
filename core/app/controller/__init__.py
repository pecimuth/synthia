from flask import Blueprint, Flask
from app.controller.schema import schema
from app.controller.auth import auth

def init_app(app: Flask):
    app.register_blueprint(schema)
    app.register_blueprint(auth)
