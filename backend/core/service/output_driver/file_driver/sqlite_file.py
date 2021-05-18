import os
import tempfile
from typing import Optional

from sqlalchemy import Table, create_engine, MetaData
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.model.meta_table import MetaTable
from core.service.data_source import DataSourceConstants
from core.service.exception import FatalDatabaseError
from core.service.generation_procedure.database import GeneratedDatabase, GeneratedRow
from core.service.output_driver.file_driver.base import FileOutputDriver


class SqliteOutputDriver(FileOutputDriver[bytes]):
    """Output file driver creating SQLite files."""

    mime_type = DataSourceConstants.MIME_TYPE_SQLITE
    display_name = 'SQLite database file'
    cli_command = 'sqlite'

    def __init__(self):
        super(SqliteOutputDriver, self).__init__()
        self._db_fd, self._db_file = tempfile.mkstemp()
        self._engine: Engine = create_engine('sqlite:///{}'.format(self._db_file))
        self._conn: Connection = self._engine.connect()
        self._current_table: Optional[Table] = None
        self._output: Optional[bytes] = None

    def start_run(self, meta: MetaData):
        meta.create_all(self._engine)

    def end_run(self, database: GeneratedDatabase):
        super(SqliteOutputDriver, self).end_run(database)
        os.close(self._db_fd)
        with open(self._db_file, 'rb') as file:
            self._output = file.read()
        os.unlink(self._db_file)

    def switch_table(self, table: Table, meta_table: MetaTable):
        self._current_table = table

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        try:
            self._conn.execute(self._current_table.insert().values(row))
        except IntegrityError:
            return None
        except SQLAlchemyError:
            os.close(self._db_fd)
            os.unlink(self._db_file)
            raise FatalDatabaseError()
        return row

    def dump(self) -> bytes:
        return self._output

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.db'.format(file_name_base)
