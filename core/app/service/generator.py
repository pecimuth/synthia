from datetime import datetime

from sqlalchemy import Table
from sqlalchemy.engine import Connection

from app.model.metacolumn import MetaColumn
from app.model.metatable import MetaTable
from app.model.project import Project
from app.service.deserializer import StructureDeserializer
from app.service.externdb import ExternDb


class Generator:

    def __init__(self, proj: Project):
        self._proj = proj
        self._deserializer = StructureDeserializer(proj)
        self._extern_db = ExternDb(proj)
        self._meta_table_dict = {
            meta_table.name : meta_table
            for meta_table in self._proj.tables
        }

    def _fill_table(self, conn: Connection, table: Table):
        meta_table = self._meta_table_dict[table.name]
        conn.execute(
            table.insert(),
            [self._make_row(meta_table) for _ in range(10)]
        )

    def fill_all(self):
        meta = self._deserializer.deserialize()
        conn = self._extern_db.engine.connect()
        for table in meta.sorted_tables:
            self._fill_table(conn, table)
        conn.close()

    @classmethod
    def _make_row(cls, meta_table: MetaTable):
        return {
            col.name : cls._make_cell(col)
            for col in meta_table.columns
            if not col.primary_key
        }

    @classmethod
    def _make_cell(cls, meta_column: MetaColumn):
        if meta_column.col_type == 'INTEGER':
            return 1
        elif meta_column.col_type == 'VARCHAR':
            return 'string'
        elif meta_column.col_type == 'DATETIME':
            return datetime.now()
        else:
            raise Exception('no generator for col type {}'.format(meta_column.col_type))
