import random

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.exception import ColumnGeneratorError
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class PrimaryKeyGenerator(ColumnGeneratorBase[int]):
    name = 'primary_key'
    only_for_type = Types.INTEGER
    is_database_generated = True

    def __init__(self, meta_column: MetaColumn):
        super().__init__(meta_column)
        self._counter = 0

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.primary_key and meta_column.col_type == Types.INTEGER

    def make_value(self,generated_database: GeneratedDatabase) -> int:
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
        return meta_column.foreign_key and meta_column.col_type == Types.INTEGER

    def make_value(self, generated_database: GeneratedDatabase) -> int:
        if generated_database.get_table_row_count(self._fk_table_name) <= 0:
            raise ColumnGeneratorError('impossible foreign key', self._meta_column)
        rows = generated_database.get_table(self._fk_table_name)
        row = random.choice(rows)
        return row[self._fk_column_name]
