from typing import List, Tuple, Iterable, Union, Any, Callable

from sqlalchemy import Table
from sqlalchemy.engine import Connection

from app.model.meta_column import MetaColumn
from app.model.meta_table import MetaTable
from app.service.generator import GeneratedDatabase, GeneratedTable, GeneratedRow
from app.service.generator.column_generator import ColumnGeneratorBase, find_recommended_generator

Generators = List[Tuple[MetaColumn, ColumnGeneratorBase]]


def _make_row(gen_table: GeneratedTable, generators: Generators) -> GeneratedRow:
    gen_row: GeneratedRow = {}
    gen_table.append(gen_row)

    for meta_column, generator in generators:
        gen_row[meta_column.name] = generator.make_value()
    return gen_row


class TableGenerator:

    def __init__(self, meta_table: MetaTable, generated_database: GeneratedDatabase):
        self._meta_table = meta_table
        self._generated_database = generated_database
        self._generators: Generators = []

    def build_with_recommended_generators(self):
        self._generators.clear()
        for meta_column in self._meta_table.columns:
            gen = find_recommended_generator(meta_column)
            # TODO improve error handling
            if gen is None:
                raise Exception('No suitable generator for {}.{}'.\
                                format(self._meta_table.name, meta_column.name))
            gen_instance = gen(self._meta_table, meta_column, self._generated_database)
            self._generators.append((meta_column, gen_instance))

    def make_table_preview(self, row_count: int) -> Iterable[GeneratedRow]:
        yield from self._make_table(row_count, True)

    def _get_appropriate_generators(self, preview: bool) -> Generators:
        filter_func: Callable[[Tuple[MetaColumn, ColumnGeneratorBase]], bool] =\
            lambda g: g[1].has_generated_value
        if preview:
            filter_func = lambda g: g[1].has_preview_value
        return list(filter(filter_func, self._generators))

    def _make_table(self, row_count: int, preview: bool) -> Iterable[GeneratedRow]:
        gen_table: GeneratedTable = []
        self._generated_database[self._meta_table.name] = gen_table
        generators = self._get_appropriate_generators(preview)
        for _ in range(row_count):
            yield _make_row(gen_table, generators)

    def _get_primary_key_column(self) -> Union[MetaColumn, None]:
        for meta_column in self._meta_table.columns:
            if meta_column.primary_key:
                return meta_column
        return None

    def fill_database(self, conn: Connection, table: Table, row_count: int):
        row_iter = self._make_table(row_count, False)
        primary_key = self._get_primary_key_column()
        for row in row_iter:
            result = conn.execute(table.insert(), row)
            # TODO we should do something like this for all generated columns
            if primary_key is not None:
                row[primary_key.name] = result.inserted_primary_key[0]
