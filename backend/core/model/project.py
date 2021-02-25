from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from core.model.meta_table import MetaTable
from . import base
from .data_source import DataSource


class Project(base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='projects')

    tables = relationship('MetaTable', order_by=MetaTable.id, back_populates='project', cascade='all, delete, delete-orphan')
    data_sources = relationship('DataSource', order_by=DataSource.id, back_populates='project', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '<Project(id={},name={},user_id={})>'.format(self.id, self.name, self.user_id)

    __table_args__ = (
        Index('ix_project_user', user_id),
    )
