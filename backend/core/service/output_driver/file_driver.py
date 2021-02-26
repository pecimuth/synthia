from io import StringIO, BytesIO
import csv
import json
from zipfile import ZIP_DEFLATED, ZipFile

from abc import abstractmethod
from typing import Union

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase, GeneratedTable
from core.service.output_driver import OutputDriver
from core.service.types import json_serialize_default


class FileOutputDriver(OutputDriver):
    is_interactive = False

    def __init__(self):
        super(FileOutputDriver, self).__init__()
        self._database: Union[GeneratedDatabase, None] = None

    def start_run(self):
        pass

    def end_run(self, database: GeneratedDatabase):
        self._database = database

    def switch_table(self, table: Table, meta_table: MetaTable):
        pass

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        return row

    @abstractmethod
    def dumps(self):
        pass

    @classmethod
    @abstractmethod
    def add_extension(cls, file_name_base: str) -> str:
        pass


class JsonOutputDriver(FileOutputDriver):
    mime_type = 'application/json'

    def dumps(self):
        return json.dumps(self._database.get_dict(), indent=2, sort_keys=True, default=json_serialize_default)

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.json'.format(file_name_base)


class ZippedCsvOutputDriver(FileOutputDriver):
    mime_type = 'application/zip'

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

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        self._writer.writerow(row)
        return row

    def dumps(self):
        self._zip_file.close()
        return self._zip_io.getvalue()

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.zip'.format(file_name_base)
