from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import base
from app.model.meta_column import MetaColumn


class MetaTable(base):
    __tablename__ = 'metatable'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project', back_populates='tables')

    columns = relationship('MetaColumn', order_by=MetaColumn.id, back_populates='table')

    row_count = Column(Integer, default=10)
