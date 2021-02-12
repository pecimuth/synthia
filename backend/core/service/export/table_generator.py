from typing import List, Tuple

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator import GeneratedRow
from core.service.column_generator.util import ColumnGeneratorBase, find_recommended_generator, \
    get_generator_by_name
from core.service.output_driver import OutputDriver

Generators = List[Tuple[MetaColumn, ColumnGeneratorBase]]


class TableGenerator:

    def __init__(self, meta_table: MetaTable, output_driver: OutputDriver):
        self._meta_table = meta_table
        self._generators: Generators = self._make_column_generators()
        self._output_driver = output_driver

    def _make_column_generators(self) -> Generators:
        result = []
        for meta_column in self._meta_table.columns:
            if meta_column.generator_name is None:
                generator_factory = find_recommended_generator(meta_column)
            else:
                generator_factory = get_generator_by_name(meta_column.generator_name)

            # TODO improve error handling
            if generator_factory is None:
                raise Exception('No suitable generator for {}.{}'.\
                                format(self._meta_table.name, meta_column.name))
            generator_instance = generator_factory(meta_column)
            result.append((meta_column, generator_instance))
        return result

    def insert_row(self) -> GeneratedRow:
        row: GeneratedRow = {}
        for meta_column, generator in self._generators:
            if not generator.is_database_generated or not self._output_driver.is_interactive:
                row[meta_column.name] = generator.make_value(self._output_driver)
        return self._output_driver.insert_row(row)
