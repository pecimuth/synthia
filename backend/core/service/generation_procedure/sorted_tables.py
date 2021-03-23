from typing import List, Set, Iterable

from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.generation_procedure.requisition import ExportRequisition


class SortedTables:
    """Sort tables according to foreign key dependencies.
    In the first try, consider all foreign keys except self-references
    and FKs pointing outside the requisition. If a cycle is detected, then
    consider only non-nullable FKs.
    """
    def __init__(self, meta_tables: List[MetaTable], requisition: ExportRequisition):
        self._requisition = requisition
        self._meta_tables = self._relevant_tables(meta_tables)
        self._cycle_detected = False

    def get_order(self) -> List[MetaTable]:
        """Return list of ordered tables, FK dependencies pointing to the right."""
        order = list(self._dfs(False))
        if self._cycle_detected:
            order = list(self._dfs(True))
        return order

    def _relevant_tables(self, meta_tables: List[MetaTable]) -> Set[MetaTable]:
        """Return set of tables in requisition."""
        result = set()
        for table in meta_tables:
            if table.name not in self._requisition:
                continue
            result.add(table)
        return result

    def _dfs(self, skip_nullable: bool) -> Iterable[MetaTable]:
        """DFS the tables, yield by sorted exit time."""
        visited = set()
        self._cycle_detected = False
        for table in self._meta_tables:
            yield from self._dfs_from(table, visited, skip_nullable)

    def _neighbors(self, start: MetaTable, skip_nullable: bool) -> Iterable[MetaTable]:
        """Return neighbors of tables, excluding itself and irrelevant tables."""
        for constraint in start.constraints:
            if constraint.constraint_type != MetaConstraint.FOREIGN:
                continue
            if skip_nullable and constraint.constrained_columns \
               and constraint.constrained_columns[0].nullable:
                continue
            if not constraint.referenced_columns:
                continue
            table = constraint.referenced_columns[0].table
            if table == start or table not in self._meta_tables:
                continue
            yield table

    def _dfs_from(self,
                  start: MetaTable,
                  visited: Set[MetaTable],
                  skip_nullable: bool) -> Iterable[MetaTable]:
        """Start DFS from a table. Yield tables sorted by exit time."""
        if start in visited:
            return []
        visited.add(start)
        for neighbor in self._neighbors(start, skip_nullable):
            if neighbor in visited:
                self._cycle_detected = True
                continue
            yield from self._dfs_from(neighbor, visited, skip_nullable)
        yield start
