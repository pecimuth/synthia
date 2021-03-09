from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class ExportRequisitionRow:
    table_name: str
    row_count: int
    seed: int


class ExportRequisition:
    def __init__(self, list_of_rows: List[ExportRequisitionRow]):
        self._rows: Dict[str, ExportRequisitionRow] = {
            row.table_name: row
            for row in list_of_rows
        }

    def number_of_rows(self, table_name: str) -> int:
        return self._rows[table_name].row_count

    def seed(self, table_name: str) -> int:
        return self._rows[table_name].seed

    def __contains__(self, table_name: str) -> bool:
        return table_name in self._rows

    @property
    def rows(self) -> Iterable[ExportRequisitionRow]:
        yield from self._rows.values()

    def __repr__(self):
        return '<ExportRequisition(rows={})>'.format(self._rows)
