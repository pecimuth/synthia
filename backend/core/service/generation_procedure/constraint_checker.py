from typing import Dict, Tuple, Set, Iterable

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.generation_procedure.database import GeneratedDatabase, GeneratedRow


class ConstraintChecker:
    def __init__(self, meta_table: MetaTable, database: GeneratedDatabase):
        self._database = database
        self._meta_table = meta_table
        self._unique_constraints: Tuple[MetaConstraint] = tuple(self._get_unique_constraints())
        self._unique_tuples: Dict[int, Set[Tuple]] = {}
        self._prepare_unique_tuples()
        self._prepare_foreign_keys()

    def _get_unique_constraints(self) -> Iterable[MetaConstraint]:
        for constraint in self._meta_table.constraints:
            if constraint.constraint_type in (MetaConstraint.UNIQUE, MetaConstraint.PRIMARY):
                yield constraint

    def _prepare_unique_tuples(self):
        for constraint in self._unique_constraints:
            self._unique_tuples[constraint.id] = set()

    def _prepare_foreign_keys(self):
        for constraint in self._meta_table.constraints:
            if constraint.constraint_type != MetaConstraint.FOREIGN:
                continue
            self._unique_tuples[constraint.id] = set()
            ref_table: MetaTable = constraint.referenced_columns[0].table
            for row in self._database.get_table(ref_table.name):
                self._insert_tuple(row, constraint.id, constraint.referenced_columns)

    @classmethod
    def _collect_tuple(cls, row: GeneratedRow, columns: Iterable[MetaColumn]) -> Tuple:
        return tuple(row[column.name] for column in columns)

    def _insert_tuple(self, row: GeneratedRow, constraint_id: int, columns: Iterable[MetaColumn]):
        unique_tuples = self._unique_tuples[constraint_id]
        row_tuple = self._collect_tuple(row, columns)
        unique_tuples.add(row_tuple)

    def _tuple_exists(self, row: GeneratedRow, constraint_id: int, columns: Iterable[MetaColumn]) -> bool:
        unique_tuples = self._unique_tuples[constraint_id]
        row_tuple = self._collect_tuple(row, columns)
        return row_tuple in unique_tuples

    def check_row(self, row: GeneratedRow) -> bool:
        for constraint in self._meta_table.constraints:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                return self._tuple_exists(row, constraint.id, constraint.constrained_columns)
            elif constraint.constraint_type in (MetaConstraint.UNIQUE, MetaConstraint.PRIMARY):
                return not self._tuple_exists(row, constraint.id, constraint.constrained_columns)
        return True

    def register_row(self, row: GeneratedRow):
        for constraint in self._unique_constraints:
            self._insert_tuple(row, constraint.id, constraint.constrained_columns)
