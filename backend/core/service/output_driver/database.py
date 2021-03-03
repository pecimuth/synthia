from typing import Union, Optional

from sqlalchemy import Table
from sqlalchemy.engine import Connection

from core.model.data_source import DataSource
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.data_source.database_common import get_shared_connection
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.output_driver import OutputDriver


class DatabaseOutputDriver(OutputDriver):
    is_interactive = True

    def __init__(self, data_source: DataSource):
        super(DatabaseOutputDriver, self).__init__()
        self._data_source = data_source
        self._conn: Optional[Connection] = None
        self._current_table: Optional[Table] = None
        self._primary_constraint: Optional[MetaConstraint] = None

    def start_run(self):
        self._conn = get_shared_connection(self._data_source)

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

    def insert_row(self, row: GeneratedRow) -> Union[GeneratedRow, None]:
        # TODO handle error
        result = self._conn.execute(self._current_table.insert().values(row))
        # TODO we should do something like this for all generated columns
        if self._primary_constraint is not None:
            inserted = result.inserted_primary_key
            for index, meta_column in enumerate(self._primary_constraint.constrained_columns):
                row[meta_column.name] = inserted[index]
        return row
