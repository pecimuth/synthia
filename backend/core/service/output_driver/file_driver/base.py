from abc import abstractmethod
from typing import TypeVar, Generic, Optional

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver import OutputDriver

DumpType = TypeVar('DumpType', str, bytes)


class FileOutputDriver(Generic[DumpType], OutputDriver):
    mime_type: str
    display_name: str
    is_interactive = False

    def __init__(self):
        super(FileOutputDriver, self).__init__()
        self._database: Optional[GeneratedDatabase] = None

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

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        return row

    @abstractmethod
    def dump(self) -> DumpType:
        pass

    @classmethod
    @abstractmethod
    def add_extension(cls, file_name_base: str) -> str:
        pass
