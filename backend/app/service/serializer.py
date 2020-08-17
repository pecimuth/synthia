from sqlalchemy import Column, Table, MetaData
from sqlalchemy.engine import Engine

from app.model.meta_column import MetaColumn
from app.model.meta_table import MetaTable
from app.model.project import Project


class StructureSerializer:

    def __init__(self, bind: Engine):
        self.meta = MetaData()
        self.meta.reflect(bind=bind)

    @classmethod
    def _make_meta_column(cls, column: Column) -> MetaColumn:
        fk = column.foreign_keys
        if len(fk) > 1:
            raise Exception('too many fks')
        fk_column = fk.pop()._get_colspec() if len(fk) == 1 else None
        return MetaColumn(
            name=column.name,
            primary_key=column.primary_key,
            col_type=column.type.__visit_name__,
            nullable=column.nullable,
            foreign_key=fk_column
        )

    @classmethod
    def _make_meta_table(cls, table: Table) -> MetaTable:
        return MetaTable(
            name=table.name,
            columns=[cls._make_meta_column(col) for col in table.c.values()]
        )

    def add_schema_to_project(self, proj: Project):
        for tab in self.meta.tables.values():
            meta_table = self._make_meta_table(tab)
            meta_table.project = proj
