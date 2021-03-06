from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from . import service
from . import controller
import os


def create_app(**kwargs) -> Flask:
    """Create, configure and return a Flask app.

    Keyword arguments may override any configuration parameter.
    """

    app = Flask(
        __name__,
        instance_relative_config=True
    )
    app.config.from_mapping(
        SWAGGER={
            'title': 'Synthia',
            'securityDefinitions': {
                'APIKeyHeader': {
                    'type': 'apiKey',
                    'name': 'Authorization',
                    'in': 'header'
                }
            }
        },
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        PROJECT_STORAGE=os.path.join(app.instance_path, 'project'),
        DATABASE_DRIVER='postgresql',
        DATABASE_USER=os.environ.get('POSTGRES_USER'),
        DATABASE_PASSWORD=os.environ.get('POSTGRES_PASSWORD'),
        DATABASE_DB=os.environ.get('POSTGRES_DB'),
        DATABASE_HOST=os.environ.get('DATABASE_HOST'),
        DATABASE_PORT=os.environ.get('DATABASE_PORT'),
        ORIGIN=os.environ.get('ORIGIN')
    )
    app.config.from_mapping(**kwargs)

    Swagger(app)
    CORS(app, origins=app.config['ORIGIN'], supports_credentials=True)

    controller.init_app(app)
    service.init_app(app)

    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['PROJECT_STORAGE'])
    except OSError:
        pass

    return app
