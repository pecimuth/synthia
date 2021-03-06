import os
import shutil
import tempfile

import pytest
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from core import model
from core.facade.project import ProjectStorage
from core.service.auth.token import SecretKey
from core.service.injector import Injector
from web import create_app
from web.service import get_db_engine
from web.service.database import create_db_engine


@pytest.fixture(scope='class')
def client() -> FlaskClient:
    db_fd, db_file = tempfile.mkstemp()
    project_storage = tempfile.mkdtemp()
    app = create_app(
        SECRET_KEY='test_key',
        PROJECT_STORAGE=project_storage,
        DATABASE_DRIVER='sqlite',
        DATABASE_USER=None,
        DATABASE_PASSWORD=None,
        DATABASE_DB=db_file,
        DATABASE_HOST=None,
        DATABASE_PORT=None,
        ORIGIN='localhost'
    )

    with app.test_client() as client:
        with app.app_context():
            model.base.metadata.create_all(get_db_engine())
        yield client

    os.close(db_fd)
    os.unlink(db_file)
    shutil.rmtree(project_storage)


@pytest.fixture(scope='class')
def session(client) -> Session:
    engine = create_db_engine(client.application)
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    finally:
        session.close()


@pytest.fixture
def injector(client, session) -> Injector:
    injector = Injector()
    injector.provide(Session, session)
    injector.provide(SecretKey, client.application.config['SECRET_KEY'])
    injector.provide(ProjectStorage, client.application.config['PROJECT_STORAGE'])
    return injector
