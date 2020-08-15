from flask import Flask
from app.controller.auth import auth
from app.controller.project import project


def init_app(app: Flask):
    app.register_blueprint(auth)
    app.register_blueprint(project)
