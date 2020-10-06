import os

from flask import current_app
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.model.project import Project


class ExternDb:

    def __init__(self, proj: Project):
        self._proj = proj
        self.engine = self._make_engine(proj)

    @classmethod
    def _make_engine(cls, proj: Project) -> Engine:
        db_path = os.path.join(current_app.config['EXTERN_DB_PATH'],
                               'project_{}.db'.format(proj.id)
                               )
        return create_engine('sqlite:///' + db_path)

    def make_session(self) -> Session:
        return sessionmaker(bind=self.engine)()
