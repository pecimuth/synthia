from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass
class ExportRequisitionRow:
    table_name: str
    row_count: int
    seed: int


class ExportRequisition:
    def __init__(self):
        self._rows: Dict[str, ExportRequisitionRow] = {}

    def extend(self, rows: Iterable[dict]):
        for row in rows:
            self.add_row(row)

    def add_row(self, row: dict):
        self._rows[row['table_name']] = ExportRequisitionRow(
            table_name=row['table_name'],
            row_count=row['row_count'],
            seed=row['seed']
        )

    def number_of_rows(self, table_name: str) -> int:
        return self._rows[table_name].row_count

    def seed(self, table_name: str) -> int:
        return self._rows[table_name].seed

    def __contains__(self, table_name: str) -> bool:
        return table_name in self._rows

    @property
    def rows(self) -> Iterable[ExportRequisitionRow]:
        yield from self._rows.values()
