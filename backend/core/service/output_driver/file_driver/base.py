from abc import abstractmethod
from typing import Union

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver import OutputDriver


class FileOutputDriver(OutputDriver):
    mime_type: str
    is_interactive = False

    def __init__(self):
        super(FileOutputDriver, self).__init__()
        self._database: Union[GeneratedDatabase, None] = None

    @classmethod
    def driver_name(cls):
        cls_name: str = cls.__name__
        suffix = 'OutputDriver'
        if cls_name.endswith(suffix):
            return cls_name[:-len(suffix)]
        return cls_name

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
