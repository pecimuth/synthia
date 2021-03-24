from typing import Dict, Any, List

GeneratedRow = Dict[str, Any]
"""Dictionary of generated values in a single row.

Keys are column names. Their respective values are the generated
values for the column.
"""

GeneratedTable = List[GeneratedRow]
"""List of generated rows in a table."""


class GeneratedDatabase:
    """Data structure holding the generated database."""

    def __init__(self):
        self._tables = {}

    def get_table(self, table_name: str) -> GeneratedTable:
        """Return generated table by name."""
        return self._tables[table_name]

    def add_table(self, table_name: str) -> GeneratedTable:
        """Add an empty table by name."""
        self._tables[table_name] = []
        return self._tables[table_name]

    def get_table_row_count(self, table_name: str) -> int:
        """Return the number of rows in a table by name.

        Return 0 for non-existing tables.
        """
        if table_name not in self._tables:
            return 0
        return len(self._tables[table_name])

    def get_dict(self) -> Dict[str, GeneratedTable]:
        """Get the data structure as a python object."""
        return self._tables

    def __contains__(self, table_name: str) -> bool:
        """Is the table with this name registered?"""
        return table_name in self._tables
