import random
from typing import Union

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
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
        if meta_column.col_type != Types.INTEGER:
            return False
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.PRIMARY:
                return True
        return False

    def make_value(self,generated_database: GeneratedDatabase) -> int:
        self._counter += 1
        return  self._counter


class ForeignKeyGenerator(ColumnGeneratorBase[int]):
    name = 'foreign_key'

    def __init__(self, meta_column: MetaColumn):
        super().__init__(meta_column)
        self._fk_column: Union[MetaColumn, None] = None
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                index = constraint.constrained_columns.index(meta_column)
                self._fk_column = constraint.referenced_columns[index]
                break

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        if meta_column.col_type != Types.INTEGER:
            return False
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                return True
        return False

    def make_value(self, generated_database: GeneratedDatabase) -> int:
        if generated_database.get_table_row_count(self._fk_column.table.name) <= 0:
            raise ColumnGeneratorError('impossible foreign key', self._meta_column)
        rows = generated_database.get_table(self._fk_column.table.name)
        row = random.choice(rows)
        return row[self._fk_column.name]
