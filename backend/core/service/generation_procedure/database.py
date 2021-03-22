from typing import Dict, Any, List

GeneratedRow = Dict[str, Any]

GeneratedTable = List[GeneratedRow]


class GeneratedDatabase:
    def __init__(self):
        self._tables = {}

    def get_table(self, table_name: str) -> GeneratedTable:
        return self._tables[table_name]

    def add_table(self, table_name: str) -> GeneratedTable:
        self._tables[table_name] = []
        return self._tables[table_name]

    def get_table_row_count(self, table_name: str) -> int:
        if table_name not in self._tables:
            return 0
        return len(self._tables[table_name])

    def get_dict(self) -> Dict[str, GeneratedTable]:
        return self._tables

    def __contains__(self, table_name: str) -> bool:
        return table_name in self._tables
