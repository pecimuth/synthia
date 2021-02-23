from sqlalchemy import Column, String, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.model import base
from core.model.meta_column import MetaColumn


class GeneratorSetting(base):
    __tablename__ = 'generatorsetting'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    params = Column(JSON)

    table_id = Column(Integer, ForeignKey('metatable.id', ondelete='CASCADE'))
    table = relationship('MetaTable', back_populates='generator_settings')

    columns = relationship('MetaColumn', order_by=MetaColumn.id, back_populates='generator_setting')
