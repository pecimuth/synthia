from datetime import date, datetime, timedelta
from io import StringIO

from typing import Union, Optional

from sqlalchemy import Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import Insert

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver.file_driver.base import FileOutputDriver


dialect = postgresql.dialect()


class LiteralCompiler(dialect.statement_compiler):
    def visit_bindparam(self,
                        bindparam,
                        within_columns_clause=False,
                        literal_binds=False,
                        **kwargs):
        return self.render_literal_value(bindparam.value, bindparam.type)

    def render_literal_value(self, value, typ):
        if value is None:
            return 'NULL'
        elif isinstance(value, (date, datetime, timedelta)):
            return str(value)
        return super(LiteralCompiler, self).render_literal_value(value, typ)


class InsertScriptOutputDriver(FileOutputDriver):
    mime_type = 'application/sql'

    def __init__(self):
        super().__init__()
        self._io = StringIO()
        self._current_table: Optional[Table] = None

    def switch_table(self, table: Table, meta_table: MetaTable):
        self._current_table = table

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        stmt = self._current_table.insert().values(row)
        self._io.write(self._stringify_stmt(stmt))
        self._io.write('\n')
        return row

    @staticmethod
    def _stringify_stmt(stmt: Insert) -> str:
        return LiteralCompiler(dialect, stmt).process(stmt)

    def end_run(self, database: GeneratedDatabase):
        super(FileOutputDriver, self).end_run(database)
        self._current_table = None

    def dumps(self):
        return self._io.getvalue()

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.sql'.format(file_name_base)
