from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.types import get_sql_alchemy_type


class StructureDeserializer:

    def __init__(self, proj: Project):
        self._proj = proj
        pass

    @classmethod
    def _deserialize_table(cls, table: MetaTable, meta: MetaData) -> Table:
        columns = [cls._deserialize_column(col) for col in table.columns]
        return Table(
            table.name,
            meta,
            *columns
        )

    @classmethod
    def _deserialize_column(cls, column: MetaColumn) -> Column:
        constraints = []
        if column.foreign_key is not None:
            constraints.append(ForeignKey(column.foreign_key))
        return Column(
            column.name,
            get_sql_alchemy_type(column.col_type),
            primary_key=column.primary_key,
            nullable=column.nullable,
            *constraints
        )

    def deserialize(self) -> MetaData:
        meta = MetaData()
        for table in self._proj.tables:
            self._deserialize_table(table, meta)
        return meta


def create_mock_meta() -> MetaData:
    meta = MetaData()
    Table('cookie', meta,
          Column('id', Integer, primary_key=True),
          Column('name', String, nullable=False),
          Column('price', Integer)
          )
    Table('order', meta,
          Column('id', Integer, primary_key=True),
          Column('place', String),
          Column('created_at', DateTime)
          )
    Table('order_item', meta,
          Column('id', Integer, primary_key=True),
          Column('order_id', Integer, ForeignKey('order.id'), nullable=False),
          Column('cookie_id', Integer, ForeignKey('cookie.id'), nullable=False),
          Column('quantity', Integer, nullable=False)
          )
    return meta
