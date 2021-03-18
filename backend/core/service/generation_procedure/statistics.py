from core.service.generation_procedure.requisition import ExportRequisition


class ProcedureTableStatistics:
    """Holds the number of requested and generated rows for a given table."""

    tolerance_factor = 2
    """
    How many failed insertions we tolerate, relative to the requested row count.
    Tolerance factor of 2 means that we will generate at most 200 rows
    if the requested count is 100.
    """

    def __init__(self, table_name: str, requested_count: int):
        self._table_name = table_name
        self._requested_count = requested_count
        self._success_count = 0
        self._insert_failure_count = 0
        self._check_failure_count = 0

    def succeed_insert(self):
        self._success_count += 1

    def fail_insert(self):
        self._insert_failure_count += 1

    def fail_check(self):
        self._check_failure_count += 1

    @property
    def satisfied(self) -> bool:
        """Have we generated successfully generated enough rows already?"""
        return self._success_count >= self._requested_count

    @property
    def attempt_count(self) -> int:
        """Return how many row generation attempts there were in total."""
        return self._success_count + self._insert_failure_count + self._check_failure_count

    @property
    def requested_count(self) -> int:
        return self._requested_count

    @property
    def expects_next_row(self) -> bool:
        """Return whether the controller should generate another row."""
        return not self.satisfied and \
            self.attempt_count < self.tolerance_factor * self.requested_count


class ProcedureStatistics:
    """Holds the number of requested and generated rows in a run."""

    def __init__(self, requisition: ExportRequisition):
        self._table_results = {
            req.table_name: ProcedureTableStatistics(req.table_name, req.row_count)
            for req in requisition.rows
        }

    def get_table_statistics(self, table_name) -> ProcedureTableStatistics:
        return self._table_results[table_name]
