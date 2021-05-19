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
    """General foreign key generator with composite key support."""

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)

        self._constraint: Optional[MetaConstraint] = None
        """Matching constraint. Constrained columns must be a superset
        of columns assigned to the generator.
        """
        self._ref_table: Optional[MetaTable] = None
        """Referenced table."""
        self._ref_column: Dict[MetaColumn, MetaColumn] = {}
        """Maps constrained columns to referenced columns."""

        columns = generator_setting.columns
        if columns:
            self._find_constraint(columns[0].constraints)

    def _find_constraint(self, constraints: List[MetaConstraint]):
        """Find a FK constraint and referenced table consistent
        with currently assigned columns.

        Sequentially try all constraints provided in the list.
        The set of constrained columns must be a superset
        of columns assigned to the generator. The referenced tables must be consistent.
        We also need to find the referenced column for each of the constrained columns.
        If no suitable constraint is found, an error is raised.
        """
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
        """Check that the referenced table matches the currently known referenced table.
        Find the referenced column. Return the status of the operation.
        """
        if meta_column not in constraint.constrained_columns:
            return False
        index = constraint.constrained_columns.index(meta_column)
        ref_column: MetaColumn = constraint.referenced_columns[index]
        if self._ref_table is None:
            self._ref_table = ref_column.table
        elif self._ref_table != ref_column.table:
            return False
        self._ref_column[meta_column] = ref_column
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
        """Return whether the column should be assigned to the generator.

        The set of constrained columns should be united.
        """
        return self._constraint is not None and \
            meta_column in self._constraint.constrained_columns

    def unite_with(self, meta_column: MetaColumn):
        """Assign the column to the generator.

        There must exist a matching constraint. Otherwise an error is raised.
        """
        super(ForeignKeyGenerator, self).unite_with(meta_column)
        if self._constraint is None:
            return self._find_constraint(meta_column.constraints)
        if not self._maybe_add_column(self._constraint, meta_column):
            raise ColumnGeneratorError('These columns do not share a FK', meta_column)

    def _all_columns_nullable(self) -> bool:
        """Are all assigned columns nullable?"""
        return all(map(lambda meta_column: meta_column.nullable, self._meta_columns))

    def _none_dict(self) -> Dict[str, None]:
        """Return dict of Nones for each column."""
        return {
            column.name: None
            for column in self._ref_column
        }

    def _from_random_row(self, rows: GeneratedTable) -> OutputDict:
        """Construct and return key from random row selected from the referenced table."""
        row = self._random.choice(rows)
        return {
            column.name: row[ref_column.name]
            for column, ref_column in self._ref_column.items()
        }

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        """Generate data for a foreign key.

        If there are no rows in the referenced table and all columns
        are nullable, we return None.
        If there are some rows, we choose randomly.
        An error is raised in other cases.
        """
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
    """Surrogate key generator.

    The numbers are generated by an interactive driver.
    In case of a non-interactive driver, the IDs are assigned sequentially
    starting from 1.
    """

    supports_null = False
    is_database_generated = True

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        self._counter = 0

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        for constraint in meta_column.constraints:
            if constraint.constraint_type == MetaConstraint.PRIMARY \
               and len(constraint.constrained_columns) == 1:
                return True
        return False

    def make_scalar(self, generated_database: GeneratedDatabase) -> int:
        self._counter += 1
        return self._counter
