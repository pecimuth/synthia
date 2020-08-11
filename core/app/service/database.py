from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from flask import current_app, g, Flask

def get_db_engine() -> Engine:
    if 'db_engine' not in g:
        g.db_engine = create_engine('sqlite:///' + current_app.config['DATABASE'])
    return g.db_engine
