from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from flask import current_app, g, Flask


def get_db_engine() -> Engine:
    if 'db_engine' not in g:
        g.db_engine = create_engine('sqlite:///' + current_app.config['DATABASE'])
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
