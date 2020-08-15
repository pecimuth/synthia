from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.model.metatable import MetaTable
from . import base


class Project(base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='projects')
    
    tables = relationship('MetaTable', order_by=MetaTable.id, back_populates='project')

    def __repr__(self):
        return '<Project(id={},name={},user_id={})>'.format(self.id, self.name, self.user_id)
