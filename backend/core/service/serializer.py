from sqlalchemy import Column, Table, MetaData
from sqlalchemy.engine import Engine

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.column_generator.util import find_recommended_generator


class StructureSerializer:

    def __init__(self, bind: Engine):
        self.meta = MetaData()
        self.meta.reflect(bind=bind)

    @classmethod
    def _with_recommended_generator(cls, meta_column: MetaColumn) -> MetaColumn:
        generator = find_recommended_generator(meta_column)
        if generator is None:
            return meta_column
        meta_column.generator_name = generator.name
        return meta_column

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
        return cls._with_recommended_generator(meta_column)

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
