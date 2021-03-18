from __future__ import annotations

import re
from typing import List, Iterable

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.exception import MalformedIdentifierError


class Identifier:
    """Uniquely identifies a column in a data source.

    The format is table name and column name joined by a dot.
    """
    PATTERN = r'^[_a-zA-Z][_a-zA-Z0-9]*$'
    COMPILED_PATTERN = re.compile(PATTERN)
    """
    In order to avoid SQL injection, we limit the table and column names.
    We only allow letters, digits and underscores.
    """

    def __init__(self, table: str, column: str):
        self._table = table
        self._column = column

        if not re.fullmatch(self.COMPILED_PATTERN, self._table):
            raise MalformedIdentifierError(self._table)
        if not re.fullmatch(self.COMPILED_PATTERN, self._column):
            raise MalformedIdentifierError(self._column)

    @property
    def table(self):
        """Table part of the identifier."""
        return self._table

    @property
    def column(self):
        """Column part of the identifier."""
        return self._column

    def __repr__(self) -> str:
        """Return the serialized identifier."""
        return '{}.{}'.format(self.table, self.column)

    @staticmethod
    def from_string(idf: str) -> Identifier:
        """Deserialize an identifier."""
        table, column = idf.split('.')
        return Identifier(table, column)

    @staticmethod
    def from_meta_column(meta_column: MetaColumn) -> Identifier:
        """Create an identifier from a meta column and its table."""
        return Identifier(meta_column.table.name, meta_column.name)


Identifiers = List[Identifier]


def structure_to_identifiers(tables: List[MetaTable]) -> Iterable[Identifier]:
    """Return list of all identifiers in a list of meta tables."""
    for table in tables:
        for column in table.columns:
            yield Identifier.from_meta_column(column)
