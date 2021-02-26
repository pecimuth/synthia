import random
from typing import Union, Any

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.service.column_generator.base import ColumnGenerator, RegisteredGenerator
from core.service.exception import ColumnGeneratorError
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class PrimaryKeyGenerator(RegisteredGenerator, ColumnGenerator[int]):
    name = 'primary_key'
    supports_null = False
    only_for_type = Types.INTEGER
    is_database_generated = True

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        self._counter = 0

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.PRIMARY:
                return True
        return False

    def make_scalar(self, generated_database: GeneratedDatabase) -> int:
        self._counter += 1
        return self._counter


class ForeignKeyGenerator(RegisteredGenerator, ColumnGenerator[Any]):
    name = 'foreign_key'

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        self._fk_column: Union[MetaColumn, None] = None
        for constraint in self._meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                index = constraint.constrained_columns.index(self._meta_column)
                self._fk_column = constraint.referenced_columns[index]
                break

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                return True
        return False

    def make_scalar(self, generated_database: GeneratedDatabase) -> Any:
        if self._fk_column is None:
            return None
        row_count = generated_database.get_table_row_count(self._fk_column.table.name)
        if row_count <= 0:
            if self._meta_column.nullable:
                return None
            raise ColumnGeneratorError('impossible foreign key', self._meta_column)
        rows = generated_database.get_table(self._fk_column.table.name)
        row = random.choice(rows)
        return row[self._fk_column.name]
