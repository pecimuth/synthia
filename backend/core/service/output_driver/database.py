from typing import Union

from sqlalchemy import Table
from sqlalchemy.engine import Connection

from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.database_common import create_database_source_engine
from core.service.generation_procedure.database import GeneratedRow
from core.service.output_driver import OutputDriver


class DatabaseOutputDriver(OutputDriver):
    is_interactive = True

    def __init__(self, data_source: DataSource):
        super(DatabaseOutputDriver, self).__init__()
        self._data_source = data_source
        self._engine = create_database_source_engine(data_source)
        self._conn: Union[Connection, None] = None
        self._current_table: Union[Table, None] = None
        self._primary_column: Union[MetaColumn, None] = None

    def start_run(self):
        self._conn = self._engine.connect()

    def end_run(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        self._primary_column = None

    def switch_table(self, table: Table, meta_table: MetaTable):
        self._current_table = table
        self._primary_column = self._get_primary_key_column(meta_table)

    @classmethod
    def _get_primary_key_column(cls, meta_table: MetaTable) -> Union[MetaColumn, None]:
        for meta_column in meta_table.columns:
            if meta_column.primary_key:
                return meta_column
        return None

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        # TODO handle error
        result = self._conn.execute(self._current_table.insert(), row)
        # TODO we should do something like this for all generated columns
        if self._primary_column is not None:
            row[self._primary_column.name] = result.inserted_primary_key[0]
        return row
