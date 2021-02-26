import json

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from flask import current_app, g

from core.service.data_source.database_common import database_connection_manager_instance
from core.service.types import json_serialize_default


def get_db_engine() -> Engine:
    if 'db_engine' not in g:
        url = URL(
            drivername=current_app.config['DATABASE_DRIVER'],
            username=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            host=current_app.config['DATABASE_HOST'],
            port=current_app.config['DATABASE_PORT'],
            database=current_app.config['DATABASE_DB']
        )
        return create_engine(
            url,
            json_serializer=lambda obj: json.dumps(obj, default=json_serialize_default)
        )
    return g.db_engine


def get_db_session_maker() -> sessionmaker:
    if 'db_session_maker' not in g:
        g.db_session_maker = sessionmaker(bind=get_db_engine())
    return g.db_session_maker


def get_db_session() -> Session:
    if 'db_session' not in g:
        g.db_session = get_db_session_maker()()
    return g.db_session


def close_db(e=None):
    session: Session = g.pop('db_session', None)
    if session is not None:
        session.close()
    database_connection_manager_instance().clean_up()
