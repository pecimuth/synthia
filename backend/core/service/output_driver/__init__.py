from abc import ABC, abstractmethod
from typing import Union

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase


class OutputDriver(ABC):
    is_interactive: bool
    cli_command: str

    @abstractmethod
    def start_run(self):
        pass

    @abstractmethod
    def end_run(self, database: GeneratedDatabase):
        pass

    @abstractmethod
    def switch_table(self, table: Table, meta_table: MetaTable):
        pass

    @abstractmethod
    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        pass


class PreviewOutputDriver(OutputDriver):
    is_interactive = False

    def start_run(self):
        pass

    def end_run(self, database: GeneratedDatabase):
        pass

    def switch_table(self, table: Table, meta_table: MetaTable):
        pass

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        return row
