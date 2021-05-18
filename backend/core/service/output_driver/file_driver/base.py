from abc import abstractmethod
from typing import TypeVar, Generic, Optional, final

from sqlalchemy import Table, MetaData

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver import OutputDriver

DumpType = TypeVar('DumpType', str, bytes)
"""The file content type of a file output driver."""


class FileOutputDriver(Generic[DumpType], OutputDriver):
    """Generic output driver for files."""

    mime_type: str
    """Mime type of the generated file."""

    display_name: str
    """The name under which the driver shows up in the GUI."""

    is_interactive = False

    def __init__(self):
        super(FileOutputDriver, self).__init__()
        self._database: Optional[GeneratedDatabase] = None

    @classmethod
    @final
    def driver_name(cls) -> str:
        """Return unambiguous identifier of the driver."""
        cls_name: str = cls.__name__
        suffix = 'OutputDriver'
        if cls_name.endswith(suffix):
            return cls_name[:-len(suffix)]
        return cls_name

    def start_run(self, meta: MetaData):
        pass

    def end_run(self, database: GeneratedDatabase):
        self._database = database

    def switch_table(self, table: Table, meta_table: MetaTable):
        pass

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        return row

    @abstractmethod
    def dump(self) -> DumpType:
        """Return file content."""
        pass

    @classmethod
    @abstractmethod
    def add_extension(cls, file_name_base: str) -> str:
        """Return new file name with an extension appended."""
        pass
