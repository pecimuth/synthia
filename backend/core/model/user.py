from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from . import base
from core.model.project import Project


class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True, unique=True)
    pwd = Column(LargeBinary, nullable=True)
    salt = Column(LargeBinary, nullable=True)
    projects = relationship('Project', order_by=Project.id, back_populates='user', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '<User(id={},email={})>'.format(self.id, self.email)
