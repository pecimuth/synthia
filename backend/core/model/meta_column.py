from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from . import base


class MetaColumn(base):
    __tablename__ = 'metacolumn'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    col_type = Column(String)
    primary_key = Column(Boolean)
    nullable = Column(Boolean)
    foreign_key = Column(String, nullable=True)

    table_id = Column(Integer, ForeignKey('metatable.id', ondelete='CASCADE'))
    table = relationship('MetaTable', back_populates='columns')

    generator_name = Column(String, nullable=True)
    generator_params = Column(JSON, nullable=True)

    data_source_id = Column(Integer, ForeignKey('datasource.id', ondelete='SET NULL'))
    data_source = relationship('DataSource')
    reflected_column_idf = Column(String, nullable=True)

    __table_args__ = (
        Index('ix_metacolumn_table_name', table_id, name, unique=True),
    )
