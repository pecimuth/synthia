import random

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.output_driver import OutputDriver


class PrimaryKeyGenerator(ColumnGeneratorBase[int]):
    name = 'primary_key'
    is_database_generated = True

    def __init__(self, meta_column: MetaColumn):
        super().__init__(meta_column)
        self._counter = 0

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.primary_key and meta_column.col_type == 'INTEGER'

    def make_value(self, output_driver: OutputDriver) -> int:
        assert not output_driver.is_interactive
        self._counter += 1
        return  self._counter


class ForeignKeyGenerator(ColumnGeneratorBase[int]):
    name = 'foreign_key'

    def __init__(self, meta_column: MetaColumn):
        super().__init__(meta_column)
        foreign_key = meta_column.foreign_key.split('.')
        assert len(foreign_key) >= 2
        self._fk_column_name = foreign_key[-1]
        self._fk_table_name = foreign_key[-2]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.foreign_key and meta_column.col_type == 'INTEGER'

    def make_value(self, output_driver: OutputDriver) -> int:
        row = random.choice(output_driver.generated_database[self._fk_table_name])
        return row[self._fk_column_name]
