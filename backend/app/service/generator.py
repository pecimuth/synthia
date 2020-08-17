import string
from datetime import datetime
from random import randint, choice

from sqlalchemy import Table
from sqlalchemy.engine import Connection

from app.model.meta_column import MetaColumn
from app.model.meta_table import MetaTable
from app.model.project import Project
from app.service.deserializer import StructureDeserializer
from app.service.extern_db import ExternDb


class Generator:

    def __init__(self, proj: Project):
        self._proj = proj
        self._deserializer = StructureDeserializer(proj)
        self._extern_db = ExternDb(proj)
        self._meta_table_dict = {
            meta_table.name : meta_table
            for meta_table in self._proj.tables
        }

    def _fill_table(self, conn: Connection, table: Table, pk_by_table: dict) -> list:
        meta_table = self._meta_table_dict[table.name]
        # returning unsupported for SQLite, would be faster
        # result = conn.execute(
        #    table.insert().returning(table.primary_key),
        #    [self._make_row(meta_table) for _ in range(10)]
        #)
        # this works for SQLite
        primary_keys = []
        for _ in range(10):
            result = conn.execute(table.insert(), self._make_row(meta_table, pk_by_table))
            pk = result.inserted_primary_key
            if len(pk) > 1:
                raise Exception('composite primary key')
            elif len(pk) == 1:
                primary_keys.append(pk[0])
        return primary_keys

    def fill_all(self):
        meta = self._deserializer.deserialize()
        conn = self._extern_db.engine.connect()
        pk_by_table = {}
        for table in meta.sorted_tables:
            pk_by_table[table.name] = self._fill_table(conn, table, pk_by_table)
        conn.close()

    @classmethod
    def _make_row(cls, meta_table: MetaTable, pk_by_table: dict):
        return {
            col.name : cls._make_cell(col, pk_by_table)
            for col in meta_table.columns
            if not col.primary_key
        }

    @classmethod
    def _make_cell(cls, meta_column: MetaColumn, pk_by_table: dict):
        if meta_column.col_type == 'INTEGER':
            if meta_column.foreign_key is None:
                return randint(0, 1000000)
            else:
                # TODO fix for FKs with schemas
                fk_table = meta_column.foreign_key[:meta_column.foreign_key.find('.')]
                return choice(pk_by_table[fk_table])
        elif meta_column.col_type == 'VARCHAR':
            return cls._make_random_string(10)
        elif meta_column.col_type == 'DATETIME':
            return datetime.now()
        else:
            raise Exception('no generator for col type {}'.format(meta_column.col_type))

    @classmethod
    def _make_random_string(cls, length: int = 10) -> str:
        return ''.join(choice(string.ascii_letters) for _ in range(length))
