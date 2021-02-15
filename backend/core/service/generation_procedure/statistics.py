from core.service.generation_procedure.requisition import TableCountRequisition


class ProcedureTableStatistics:
    def __init__(self, table_name: str, requested_count: int):
        self._table_name = table_name
        self._requested_count = requested_count
        self._success_count = 0
        self._failure_count = 0

    def succeed_insert(self):
        self._success_count += 1

    def fail_insert(self):
        self._failure_count += 1

    @property
    def satisfied(self) -> bool:
        return self._success_count >= self._requested_count

    @property
    def attempt_count(self) -> int:
        return self._success_count + self._failure_count

    @property
    def requested_count(self) -> int:
        return self._requested_count

    @property
    def expects_next_row(self) -> int:
        return not self.satisfied and self.attempt_count < 2 * self.requested_count


class ProcedureStatistics:
    def __init__(self, requisition: TableCountRequisition):
        self._table_results = {
            table_name: ProcedureTableStatistics(table_name, count)
            for table_name, count in requisition.items()
        }

    def get_table_statistics(self, table_name) -> ProcedureTableStatistics:
        return self._table_results[table_name]
