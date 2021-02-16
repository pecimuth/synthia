from typing import List

from sqlalchemy import Column, Table, MetaData

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.database_common import create_database_source_engine
from core.service.data_source.identifier import Identifier
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.types import get_column_type


class DatabaseSchemaProvider(SchemaProvider):
    def read_structure(self) -> List[MetaTable]:
        engine = create_database_source_engine(self._data_source)
        meta = MetaData()
        meta.reflect(bind=engine)
        return [
            self._make_meta_table(tab)
            for tab in meta.tables.values()
        ]

    def _make_meta_column(self, table: Table, column: Column) -> MetaColumn:
        fk = column.foreign_keys
        if len(fk) > 1:
            raise Exception('too many fks')
        fk_column = fk.pop()._get_colspec() if len(fk) == 1 else None
        meta_column = MetaColumn(
            name=column.name,
            primary_key=column.primary_key,
            col_type=get_column_type(column),
            nullable=column.nullable,
            foreign_key=fk_column,
            data_source=self._data_source,
            reflected_column_idf=repr(Identifier(table.name, column.name))
        )
        self._set_recommended_generator(meta_column)
        return meta_column

    def _make_meta_table(self, table: Table) -> MetaTable:
        return MetaTable(
            name=table.name,
            columns=[
                self._make_meta_column(table, col)
                for col in table.c.values()
            ]
        )
