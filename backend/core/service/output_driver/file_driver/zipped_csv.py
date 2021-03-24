from io import StringIO, BytesIO
import csv
from zipfile import ZIP_DEFLATED, ZipFile

from typing import Optional, Dict

from attr import dataclass
from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver.file_driver.base import FileOutputDriver


@dataclass
class TableIoWriter:
    """Table writer and its output IO."""
    writer: csv.DictWriter
    io: StringIO


class ZippedCsvOutputDriver(FileOutputDriver[bytes]):
    """Output file driver creating zipped CSV files per table."""

    mime_type = 'application/zip'
    display_name = 'Zipped CSV'
    cli_command = 'zip'

    def __init__(self):
        super(ZippedCsvOutputDriver, self).__init__()
        self._zip_io = BytesIO()
        self._zip_file = ZipFile(self._zip_io, 'w', ZIP_DEFLATED, False)
        self._table_ios: Dict[MetaTable, TableIoWriter] = {}
        self._writer: Optional[csv.DictWriter] = None

    def _write_tables_to_zip_file(self):
        for meta_table, io_writer in self._table_ios.items():
            file_name = '{}.csv'.format(meta_table.name)
            table_str = io_writer.io.getvalue()
            self._zip_file.writestr(file_name, table_str)
            io_writer.io.close()

    def end_run(self, database: GeneratedDatabase):
        super(ZippedCsvOutputDriver, self).end_run(database)
        self._write_tables_to_zip_file()
        for file in self._zip_file.filelist:
            file.create_system = 0

    def switch_table(self, table: Table, meta_table: MetaTable):
        if meta_table in self._table_ios:
            self._writer = self._table_ios[meta_table].writer
            return
        # we see the table for the first time: create IO, writer, header
        io = StringIO()
        fields = list(map(lambda col: col.name, meta_table.columns))
        self._writer = csv.DictWriter(io, fieldnames=fields, quoting=csv.QUOTE_NONNUMERIC)
        self._table_ios[meta_table] = TableIoWriter(writer=self._writer, io=io)
        self._writer.writeheader()

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        self._writer.writerow(row)
        return row

    def dump(self) -> bytes:
        self._zip_file.close()
        return self._zip_io.getvalue()

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.zip'.format(file_name_base)
