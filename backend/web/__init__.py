from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from . import service
from . import controller
import os


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SWAGGER={
            'title': 'Synthia'
        },
        SECRET_KEY=os.environ['SECRET_KEY'],
        EXTERN_DB_PATH=os.path.join(app.instance_path, 'extern/'),
        PROJECT_STORAGE=os.path.join(app.instance_path, 'project'),
        DATABASE_DRIVER='postgresql',
        DATABASE_USER=os.environ['POSTGRES_USER'],
        DATABASE_PASSWORD=os.environ['POSTGRES_PASSWORD'],
        DATABASE_DB=os.environ['POSTGRES_DB'],
        DATABASE_HOST=os.environ['DATABASE_HOST'],
        DATABASE_PORT=os.environ['DATABASE_PORT'],
        ORIGIN=os.environ['ORIGIN']
    )

    Swagger(app)
    CORS(app, origins=app.config['ORIGIN'], supports_credentials=True)

    controller.init_app(app)
    service.init_app(app)

    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['PROJECT_STORAGE'])
        os.makedirs(app.config['EXTERN_DB_PATH'])
    except OSError:
        pass

    return app
