from typing import Optional

from sqlalchemy import Table
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.data_source.database_common import DatabaseConnectionManager, DataSourceOrUrl
from core.service.exception import FatalDatabaseError
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver import OutputDriver


class DatabaseOutputDriver(OutputDriver):
    is_interactive = True
    cli_command = 'insert'

    def __init__(self, data_source_url: DataSourceOrUrl, conn_manager: DatabaseConnectionManager):
        super(DatabaseOutputDriver, self).__init__()
        self._data_source_url = data_source_url
        self._conn_manager = conn_manager
        self._conn: Optional[Connection] = None
        self._current_table: Optional[Table] = None
        self._primary_constraint: Optional[MetaConstraint] = None

    def start_run(self):
        self._conn = self._conn_manager.get_connection(self._data_source_url)

    def end_run(self, database: GeneratedDatabase):
        self._conn = None
        self._primary_constraint = None

    def switch_table(self, table: Table, meta_table: MetaTable):
        self._current_table = table
        self._find_primary_constraint(meta_table)

    def _find_primary_constraint(self, meta_table: MetaTable):
        self._primary_constraint = None
        for constraint in meta_table.constraints:
            if constraint.constraint_type == MetaConstraint.PRIMARY:
                self._primary_constraint = constraint
                return

    def insert_row(self, row: GeneratedRow) -> Optional[GeneratedRow]:
        try:
            result = self._conn.execute(self._current_table.insert().values(row))
        except IntegrityError:
            return None
        except SQLAlchemyError:
            raise FatalDatabaseError()
        if self._primary_constraint is not None:
            inserted = result.inserted_primary_key
            for index, meta_column in enumerate(self._primary_constraint.constrained_columns):
                row[meta_column.name] = inserted[index]
        return row
