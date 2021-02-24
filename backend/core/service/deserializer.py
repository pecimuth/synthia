from typing import Any, List

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.types import get_sql_alchemy_type


class StructureDeserializer:

    def __init__(self, proj: Project):
        self._proj = proj

    @classmethod
    def _deserialize_table(cls, meta_table: MetaTable, meta: MetaData) -> Table:
        columns = [cls._deserialize_column(col) for col in meta_table.columns]
        constraints = cls._make_fk_constraints(meta_table)
        table = Table(
            meta_table.name,
            meta,
            *columns,
            *constraints
        )
        return table

    @classmethod
    def _deserialize_column(cls, meta_column: MetaColumn) -> Column:
        column = Column(
            meta_column.name,
            get_sql_alchemy_type(meta_column.col_type),
            nullable=meta_column.nullable
        )
        return column

    @classmethod
    def _make_fk_constraints(cls, meta_table: MetaTable) -> List[ForeignKeyConstraint]:
        constraints = []
        for meta_constraint in meta_table.constraints:
            if meta_constraint.constraint_type != MetaConstraint.FOREIGN:
                continue
            constrained_columns: Any = [
                meta_column.name
                for meta_column in meta_constraint.constrained_columns
            ]
            referenced_columns = [
                '{}.{}'.format(meta_column.table.name, meta_column.name)
                for meta_column in meta_constraint.referenced_columns
            ]
            constraint = ForeignKeyConstraint(
                constrained_columns,
                referenced_columns,
                name=meta_constraint.name
            )
            constraints.append(constraint)
        return constraints

    def deserialize(self) -> MetaData:
        meta = MetaData()
        for table in self._proj.tables:
            self._deserialize_table(table, meta)
        return meta


def create_mock_meta() -> MetaData:
    meta = MetaData()
    Table(
        'cookie',
        meta,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('price', Integer)
    )
    Table(
        'order',
        meta,
        Column('id', Integer, primary_key=True),
        Column('place', String),
        Column('created_at', DateTime)
    )
    Table(
        'order_item',
        meta,
        Column('id', Integer, primary_key=True),
        Column('order_id', Integer, ForeignKey('order.id'), nullable=False),
        Column('cookie_id', Integer, ForeignKey('cookie.id'), nullable=False),
        Column('quantity', Integer, nullable=False)
    )
    return meta
