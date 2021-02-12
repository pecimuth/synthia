from typing import Union

from sqlalchemy import Table
from sqlalchemy.engine import Connection

from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.database import create_database_source_engine
from core.service.column_generator import GeneratedRow
from core.service.output_driver import OutputDriver, MetaTableCounts


class DatabaseOutputDriver(OutputDriver):
    is_interactive = True

    def __init__(self, data_source: DataSource, meta_table_counts: MetaTableCounts):
        super().__init__(data_source.project, meta_table_counts)
        self._data_source = data_source
        self._engine = create_database_source_engine(data_source)
        self._conn: Union[Connection, None] = None
        self._primary_column: Union[MetaColumn, None] = None

    def _on_generation_begin(self):
        super(DatabaseOutputDriver, self)._on_generation_begin()
        self._conn = self._engine.connect()

    def _on_generation_end(self):
        super(DatabaseOutputDriver, self)._on_generation_end()
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        self._primary_column = None

    def _on_next_table(self, table: Table, meta_table: MetaTable, n_rows: int):
        super(DatabaseOutputDriver, self)._on_next_table(table, meta_table, n_rows)
        self._primary_column = self._get_primary_key_column(meta_table)

    @classmethod
    def _get_primary_key_column(cls, meta_table: MetaTable) -> Union[MetaColumn, None]:
        for meta_column in meta_table.columns:
            if meta_column.primary_key:
                return meta_column
        return None

    def insert_row(self, row: GeneratedRow) -> GeneratedRow:
        # TODO handle error
        result = self._conn.execute(self._current_table.insert(), row)
        # TODO we should do something like this for all generated columns
        if self._primary_column is not None:
            row[self._primary_column.name] = result.inserted_primary_key[0]
        return super(DatabaseOutputDriver, self).insert_row(row)
