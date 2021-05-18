from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import Table, MetaData

from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase


class OutputDriver(ABC):
    """Process output data."""

    is_interactive: bool
    """Can generate database-generated values?"""

    cli_command: str
    """Identifier, which makes the driver available from CLI."""

    @abstractmethod
    def start_run(self, meta: MetaData):
        """Start the data generation run.

        Should be called once at the beginning of each run.
        """
        pass

    @abstractmethod
    def end_run(self, database: GeneratedDatabase):
        """End the data generation run.

        Called at the end of each run.
        """
        pass

    @abstractmethod
    def switch_table(self, table: Table, meta_table: MetaTable):
        """The next row will belong to this table/meta_table."""
        pass

    @abstractmethod
    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        """Insert the row to a table. Returns None on failure.
        Complete row is returned on success.

        In case of interactive drivers, it may have more entries
        compare to the original row."""
        pass


class PreviewOutputDriver(OutputDriver):
    """Output driver for data preview. Has no effect."""
    is_interactive = False

    def start_run(self, meta: MetaData):
        pass

    def end_run(self, database: GeneratedDatabase):
        pass

    def switch_table(self, table: Table, meta_table: MetaTable):
        pass

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        return row
