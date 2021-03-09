from io import StringIO, BytesIO
import csv
from zipfile import ZIP_DEFLATED, ZipFile

from typing import Optional

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver.file_driver.base import FileOutputDriver


class ZippedCsvOutputDriver(FileOutputDriver[bytes]):
    mime_type = 'application/zip'
    display_name = 'Zipped CSV'
    cli_command = 'zip'

    def __init__(self):
        super(ZippedCsvOutputDriver, self).__init__()
        self._zip_io = BytesIO()
        self._zip_file = ZipFile(self._zip_io, 'w', ZIP_DEFLATED, False)
        self._table_io = None
        self._writer = None
        self._last_table_name = None

    def _write_table_to_zip_file(self):
        if self._table_io is not None:
            file_name = '{}.csv'.format(self._last_table_name)
            table_str = self._table_io.getvalue()
            self._zip_file.writestr(file_name, table_str)
            self._table_io.close()

    def end_run(self, database: GeneratedDatabase):
        super(ZippedCsvOutputDriver, self).end_run(database)
        self._write_table_to_zip_file()
        for file in self._zip_file.filelist:
            file.create_system = 0
        self._table_io = None
        self._writer = None
        self._last_table_name = None

    def switch_table(self, table: Table, meta_table: MetaTable):
        self._write_table_to_zip_file()
        self._table_io = StringIO()
        fields = list(map(lambda col: col.name, meta_table.columns))
        self._writer = csv.DictWriter(self._table_io, fieldnames=fields)
        self._writer.writeheader()
        self._last_table_name = meta_table.name

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        self._writer.writerow(row)
        return row

    def dump(self) -> bytes:
        self._zip_file.close()
        return self._zip_io.getvalue()

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.zip'.format(file_name_base)
