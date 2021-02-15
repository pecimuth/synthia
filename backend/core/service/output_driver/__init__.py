from abc import ABC, abstractmethod
from typing import Union

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow


class OutputDriver(ABC):
    is_interactive: bool

    @abstractmethod
    def start_run(self):
        pass

    @abstractmethod
    def end_run(self):
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

    def end_run(self):
        pass

    def switch_table(self, table: Table, meta_table: MetaTable):
        pass

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        return row
