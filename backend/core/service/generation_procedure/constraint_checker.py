from typing import Dict, Tuple, Set, Iterable, List

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.generation_procedure.database import GeneratedDatabase, GeneratedRow


class ConstraintChecker:
    def __init__(self, project: Project, database: GeneratedDatabase, interactive_driver: bool):
        self._project = project
        self._database = database
        self._interactive_driver = interactive_driver
        self._watched_by_table: Dict[MetaTable, List[MetaConstraint]] = {
            table: [] for table in self._project.tables
        }
        self._unique_tuples: Dict[MetaConstraint, Set[Tuple]] = {}
        self._prepare()

    def _prepare(self):
        for meta_table in self._project.tables:
            for constraint in meta_table.constraints:
                if constraint.constraint_type not in (MetaConstraint.FOREIGN,
                                                      MetaConstraint.PRIMARY,
                                                      MetaConstraint.UNIQUE):
                    continue
                self._unique_tuples[constraint] = set()
                ref_table = meta_table
                if constraint.constraint_type == MetaConstraint.FOREIGN:
                    if not constraint.referenced_columns[0]:
                        continue
                    ref_table = constraint.referenced_columns[0].table
                self._watched_by_table[ref_table].append(constraint)

    @classmethod
    def _is_unique_constraint(cls, constraint: MetaConstraint) -> bool:
        return constraint.constraint_type in (MetaConstraint.UNIQUE, MetaConstraint.PRIMARY)

    def _should_check_uniqueness(self, constraint: MetaConstraint) -> bool:
        return constraint.constraint_type == MetaConstraint.UNIQUE or \
               (constraint.constraint_type == MetaConstraint.PRIMARY and not self._interactive_driver)

    @classmethod
    def _collect_tuple(cls, row: GeneratedRow, columns: Iterable[MetaColumn]) -> Tuple:
        return tuple(row[column.name] for column in columns)

    def _insert_tuple(self, row: GeneratedRow, constraint: MetaConstraint, columns: Iterable[MetaColumn]):
        unique_tuples = self._unique_tuples[constraint]
        row_tuple = self._collect_tuple(row, columns)
        unique_tuples.add(row_tuple)

    def _tuple_exists(self, row: GeneratedRow, constraint: MetaConstraint, columns: Iterable[MetaColumn]) -> bool:
        unique_tuples = self._unique_tuples[constraint]
        row_tuple = self._collect_tuple(row, columns)
        return row_tuple in unique_tuples

    def _tuple_is_none(self, row: GeneratedRow, columns: Iterable[MetaColumn]) -> bool:
        row_tuple = self._collect_tuple(row, columns)
        return all(map(lambda elem: elem is None, row_tuple))

    def check_row(self, meta_table: MetaTable, row: GeneratedRow) -> bool:
        for constraint in meta_table.constraints:
            if constraint not in self._unique_tuples:
                continue

            if constraint.constraint_type == MetaConstraint.FOREIGN \
               and not self._tuple_is_none(row, constraint.constrained_columns) \
               and not self._tuple_exists(row, constraint, constraint.constrained_columns):
                return False
            elif self._should_check_uniqueness(constraint) \
                    and not self._tuple_is_none(row, constraint.constrained_columns) \
                    and self._tuple_exists(row, constraint, constraint.constrained_columns):
                return False
        for meta_column in meta_table.columns:
            if not meta_column.nullable and \
               meta_column.name in row and \
               row[meta_column.name] is None:
                return False
        return True

    def register_row(self, meta_table: MetaTable, row: GeneratedRow):
        for constraint in self._watched_by_table[meta_table]:
            if constraint.constraint_type == MetaConstraint.FOREIGN:
                columns = constraint.referenced_columns
            else:
                columns = constraint.constrained_columns
            self._insert_tuple(row, constraint, columns)
