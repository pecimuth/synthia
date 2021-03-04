from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from . import base
from core.model.meta_column import MetaColumn
from .generator_setting import GeneratorSetting
from .meta_constraint import MetaConstraint


class MetaTable(base):
    __tablename__ = 'metatable'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project', back_populates='tables')

    columns = relationship('MetaColumn',
                           order_by=MetaColumn.id,
                           back_populates='table',
                           cascade='all, delete, delete-orphan')

    generator_settings = relationship('GeneratorSetting',
                                      order_by=GeneratorSetting.id,
                                      back_populates='table',
                                      cascade='all, delete, delete-orphan')

    data_source_id = Column(Integer, ForeignKey('datasource.id', ondelete='SET NULL'))
    data_source = relationship('DataSource')

    constraints = relationship('MetaConstraint', order_by=MetaConstraint.id, back_populates='table')

    __table_args__ = (
        Index('ix_metatable_project_name', project_id, name, unique=True),
    )

    def __repr__(self):
        return '<MetaTable(id={},name={},columns={},constraints={},generator_settings={})>'.format(
            self.id,
            self.name,
            self.columns,
            self.constraints,
            self.generator_settings
        )
