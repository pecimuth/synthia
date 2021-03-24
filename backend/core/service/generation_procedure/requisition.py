from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class ExportRequisitionRow:
    """Export requisition for a single table."""

    table_name: str
    """The name of the table."""

    row_count: int
    """How many rows should be generated."""

    seed: int
    """Primary seed for the column generators."""


class ExportRequisition:
    """Complete export requisition consisting of table requisitions."""

    def __init__(self, list_of_rows: List[ExportRequisitionRow]):
        self._rows: Dict[str, ExportRequisitionRow] = {
            row.table_name: row
            for row in list_of_rows
        }
        """Dictionary of table export requisitions by table names."""

    def number_of_rows(self, table_name: str) -> int:
        """Return the requested number of rows for a given table by name."""
        return self._rows[table_name].row_count

    def seed(self, table_name: str) -> int:
        """Return the requested seed for a given table by name."""
        return self._rows[table_name].seed

    def __contains__(self, table_name: str) -> bool:
        """Is the table included in the requisition?"""
        return table_name in self._rows

    @property
    def rows(self) -> Iterable[ExportRequisitionRow]:
        """Return an iterable of table export requisitions."""
        yield from self._rows.values()

    def __repr__(self):
        return '<ExportRequisition(rows={})>'.format(self._rows)
