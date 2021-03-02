from typing import List, Union, Dict

from sqlalchemy import Column, Table, MetaData, Constraint, CheckConstraint, UniqueConstraint, PrimaryKeyConstraint, \
    ForeignKeyConstraint

from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.data_source.database_common import get_shared_engine
from core.service.data_source.identifier import Identifier
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.exception import SomeError
from core.service.types import get_column_type


class DatabaseSchemaProvider(SchemaProvider):
    def __init__(self, data_source: DataSource):
        super().__init__(data_source)
        self._table_list: Union[List[MetaTable], None] = []
        self._column: Dict[str, Dict[str, MetaColumn]] = {}

    def read_structure(self) -> List[MetaTable]:
        engine = get_shared_engine(self._data_source)
        meta = MetaData()
        meta.reflect(bind=engine)
        self._column = {}
        self._table_list = [
            self._make_meta_table(tab)
            for tab in meta.tables.values()
        ]
        self._add_meta_constraints(meta)
        return self._table_list

    def _make_meta_column(self, table: Table, column: Column) -> MetaColumn:
        meta_column = MetaColumn(
            name=column.name,
            col_type=get_column_type(column),
            nullable=column.nullable,
            data_source=self._data_source,
            reflected_column_idf=repr(Identifier(table.name, column.name))
        )
        return meta_column

    def _make_meta_table(self, table: Table) -> MetaTable:
        meta_table = MetaTable(name=table.name, columns=[])
        self._column[table.name] = {}
        for col in table.c.values():
            try:
                meta_column = self._make_meta_column(table, col)
                meta_table.columns.append(meta_column)
                self._column[table.name][col.name] = meta_column
            except SomeError:
                # TODO maybe add a message
                pass
        return meta_table

    def _add_meta_constraints(self, meta: MetaData):
        for meta_table, table in zip(self._table_list, meta.tables.values()):
            for constraint in table.constraints:
                meta_constraint = self._make_meta_constraint(meta_table, constraint)
                meta_table.constraints.append(meta_constraint)

    def _make_meta_constraint(self, meta_table: MetaTable, constraint: Constraint) -> MetaConstraint:
        meta_constraint = MetaConstraint(
            name=constraint.name,
            table=meta_table,
            constrained_columns=[],
            referenced_columns=[]
        )
        if hasattr(constraint, 'columns'):
            column_by_name = self._column[meta_table.name]
            for column in constraint.columns:
                meta_column = column_by_name[column.name]
                meta_constraint.constrained_columns.append(meta_column)
        if isinstance(constraint, CheckConstraint):
            meta_constraint.constraint_type = MetaConstraint.CHECK
            meta_constraint.check_expression = str(constraint.sqltext)
        elif isinstance(constraint, UniqueConstraint):
            meta_constraint.constraint_type = MetaConstraint.UNIQUE
        elif isinstance(constraint, PrimaryKeyConstraint):
            meta_constraint.constraint_type = MetaConstraint.PRIMARY
        elif isinstance(constraint, ForeignKeyConstraint):
            meta_constraint.constraint_type = MetaConstraint.FOREIGN
            for foreign_key in constraint.elements:
                column_by_name = self._column[foreign_key.column.table.name]
                meta_column = column_by_name[foreign_key.column.name]
                meta_constraint.referenced_columns.append(meta_column)
        else:
            raise SomeError('unknown constraint type')
        return meta_constraint
