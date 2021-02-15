from typing import List

from sqlalchemy import Column, Table, MetaData

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.database_common import create_database_source_engine
from core.service.data_source.schema.base_provider import SchemaProvider


class DatabaseSchemaProvider(SchemaProvider):
    def read_structure(self) -> List[MetaTable]:
        engine = create_database_source_engine(self._data_source)
        meta = MetaData()
        meta.reflect(bind=engine)
        return [
            self._make_meta_table(tab)
            for tab in meta.tables.values()
        ]

    @classmethod
    def _make_meta_column(cls, column: Column) -> MetaColumn:
        fk = column.foreign_keys
        if len(fk) > 1:
            raise Exception('too many fks')
        fk_column = fk.pop()._get_colspec() if len(fk) == 1 else None
        meta_column = MetaColumn(
            name=column.name,
            primary_key=column.primary_key,
            col_type=column.type.__visit_name__,
            nullable=column.nullable,
            foreign_key=fk_column
        )
        cls._set_recommended_generator(meta_column)
        return meta_column

    @classmethod
    def _make_meta_table(cls, table: Table) -> MetaTable:
        return MetaTable(
            name=table.name,
            columns=[cls._make_meta_column(col) for col in table.c.values()]
        )
