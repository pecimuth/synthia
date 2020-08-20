from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from . import service
from . import controller
import os


def create_app(test_config=None) -> Flask:

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SWAGGER={
            'title': 'Synthia'
        },
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'data.db'),
        EXTERN_DB_PATH=os.path.join(app.instance_path, 'extern/'),
        ORIGINS='http://localhost:4200'
    )

    Swagger(app)
    CORS(app, origins=app.config['ORIGINS'], supports_credentials=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    controller.init_app(app)
    service.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config['EXTERN_DB_PATH'])
    except OSError:
        pass

    return app