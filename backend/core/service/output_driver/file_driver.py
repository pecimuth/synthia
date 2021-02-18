import json
from abc import abstractmethod
from typing import Union

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver import OutputDriver


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
    def dumps(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def add_extension(cls, file_name_base: str) -> str:
        pass


class JsonOutputDriver(FileOutputDriver):
    mime_type = 'application/json'

    def dumps(self) -> str:
        return json.dumps(self._database.get_dict())

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.json'.format(file_name_base)
