from sqlalchemy import Column, Integer, String
from . import base

class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)

    def __repr__(self):
        return '<User(id={},email={})>'.format(self.id, self.email)
