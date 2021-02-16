from typing import List, Iterable

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable


class Identifier:
    def __init__(self, table: str, column: str):
        self._table = table
        self._column = column

    @property
    def table(self):
        return self._table

    @property
    def column(self):
        return self._column

    def __repr__(self):
        return '{}.{}'.format(self.table, self.column)


def identifier_from_string(idf: str):
    table, column = idf.split('.')
    return Identifier(table, column)


def identifier_from_meta_column(meta_column: MetaColumn):
    return Identifier(meta_column.table.name, meta_column.name)


def structure_to_identifiers(tables: List[MetaTable]) -> Iterable[Identifier]:
    for table in tables:
        for column in table.columns:
            yield identifier_from_meta_column(column)
