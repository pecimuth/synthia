from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import base


class MetaColumn(base):
    __tablename__ = 'metacolumn'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    col_type = Column(String)
    primary_key = Column(Boolean)
    nullable = Column(Boolean)

    table_id = Column(Integer, ForeignKey('metatable.id'))
    table = relationship('MetaTable', back_populates='columns')
