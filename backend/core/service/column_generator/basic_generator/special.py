from typing import Optional, Dict, List

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.column_generator.base import RegisteredGenerator, SingleColumnGenerator, MultiColumnGenerator, \
    OutputDict
from core.service.exception import ColumnGeneratorError, GeneratorSettingError
from core.service.generation_procedure.database import GeneratedDatabase, GeneratedTable
from core.service.types import Types


class ForeignKeyGenerator(RegisteredGenerator, MultiColumnGenerator):

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)

        self._constraint: Optional[MetaConstraint] = None
        self._ref_table: Optional[MetaTable] = None
        self._ref_column: Dict[str, MetaColumn] = {}

        columns = generator_setting.columns
        if columns:
            self._find_constraint(columns[0].constraints)

    def _find_constraint(self, constraints: List[MetaConstraint]):
        for constraint in constraints:
            if constraint.constraint_type != MetaConstraint.FOREIGN:
                continue
            self._ref_table = None
            self._ref_column.clear()
            for meta_column in self._meta_columns:
                if not self._maybe_add_column(constraint, meta_column):
                    continue
            self._constraint = constraint
            return
        raise GeneratorSettingError(
            'No appropriate FK constraint found',
            self._generator_setting
        )

    def _maybe_add_column(self, constraint: MetaConstraint, meta_column: MetaColumn) -> bool:
        if meta_column not in constraint.constrained_columns:
            return False
        index = constraint.constrained_columns.index(meta_column)
        ref_column: MetaColumn = constraint.referenced_columns[index]
        if self._ref_table is None:
            self._ref_table = ref_column.table
        elif self._ref_table != ref_column.table:
            return False
        self._ref_column[meta_column.name] = ref_column
        return True

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return None

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                return True
        return False

    def should_unite_with(self, meta_column: MetaColumn) -> bool:
        return self._constraint is not None and \
            meta_column in self._constraint.constrained_columns

    def unite_with(self, meta_column: MetaColumn):
        super(ForeignKeyGenerator, self).unite_with(meta_column)
        if self._constraint is None:
            return self._find_constraint(meta_column.constraints)
        if not self._maybe_add_column(self._constraint, meta_column):
            raise ColumnGeneratorError('These columns do not share a FK', meta_column)

    def _all_columns_nullable(self) -> bool:
        return all(map(lambda meta_column: meta_column.nullable, self._meta_columns))

    def _none_dict(self) -> Dict[str, None]:
        return {
            name: None
            for name in self._ref_column
        }

    def _from_random_row(self, rows: GeneratedTable) -> OutputDict:
        row = self._random.choice(rows)
        return {
            name: row[ref_column.name]
            for name, ref_column in self._ref_column.items()
        }

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        if not self._constraint:
            raise GeneratorSettingError('Dangling FK generator', self._generator_setting)

        row_count = generated_database.get_table_row_count(self._ref_table.name)
        if row_count == 0:
            if self._all_columns_nullable():
                return self._none_dict()
            raise GeneratorSettingError(
                'Impossible foreign key',
                self._generator_setting
            )

        rows = generated_database.get_table(self._ref_table.name)
        return self._from_random_row(rows)


class PrimaryKeyGenerator(RegisteredGenerator, SingleColumnGenerator[int]):
    supports_null = False
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
