from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from . import base
from core.model.meta_column import MetaColumn


class MetaTable(base):
    __tablename__ = 'metatable'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project', back_populates='tables')

    columns = relationship('MetaColumn', order_by=MetaColumn.id, back_populates='table')

    data_source_id = Column(Integer, ForeignKey('datasource.id', ondelete='SET NULL'))
    data_source = relationship('DataSource')

    __table_args__ = (
        Index('ix_metatable_project_name', project_id, name, unique=True),
    )
