from collections import deque
from typing import Iterable, Tuple, Optional

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.column_generator.setting_facade import GeneratorSettingFacade, GeneratorList
from core.service.deserializer import StructureDeserializer
from core.service.generation_procedure.constraint_checker import ConstraintChecker
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.generation_procedure.requisition import ExportRequisition
from core.service.generation_procedure.sorted_tables import SortedTables
from core.service.generation_procedure.statistics import ProcedureStatistics
from core.service.output_driver import OutputDriver


class ProcedureController:
    def __init__(self,
                 project: Project,
                 requisition: ExportRequisition,
                 output_driver: OutputDriver):
        self._project = project
        self._statistics = ProcedureStatistics(requisition)
        self._requisition = requisition
        self._output_driver = output_driver
        self._database: Optional[GeneratedDatabase] = None
        self._checker: Optional[ConstraintChecker] = None

    def run(self) -> GeneratedDatabase:
        """Generate the data according to the requisition using
        the provided output driver. Return the generated data.
        """
        self._database = GeneratedDatabase()
        self._checker = ConstraintChecker(self._project,
                                          self._database,
                                          self._output_driver.is_interactive)
        self._output_driver.start_run()
        states = deque((iter(self._table_loop(meta_table)), table, meta_table)
                       for table, meta_table in self._sorted_tables())
        while states:
            it, table, meta_table = states.popleft()
            self._output_driver.switch_table(table, meta_table)
            try:
                next(it)
                states.append((it, table, meta_table))
            except StopIteration:
                pass
        self._output_driver.end_run(self._database)
        return self._database

    def _sorted_tables(self) -> Iterable[Tuple[Table, MetaTable]]:
        """Return pairs of SQL Alchemy tables and MetaTables
        in order of foreign key dependencies.
        """
        deserializer = StructureDeserializer(self._project)
        meta = deserializer.deserialize()
        table_by_name = {
            name: table
            for name, table in meta.tables.items()
        }
        sorted_tables = SortedTables(self._project.tables, self._requisition)
        for meta_table in sorted_tables.get_order():
            yield table_by_name[meta_table.name], meta_table

    def _table_loop(self, meta_table: MetaTable) -> Iterable[GeneratedRow]:
        """Create generators for a given table and fill it with data,
        while checking the integrity constraints.

        Yield complete row after each successful insert.
        """
        table_db = self._database.add_table(meta_table.name)
        stats = self._statistics.get_table_statistics(meta_table.name)
        generators = GeneratorSettingFacade.instances_from_table(meta_table)
        table_seed = self._requisition.seed(meta_table.name)
        GeneratorSettingFacade.seed_all(generators, table_seed)
        while stats.expects_next_row:
            row = self._make_row(generators)
            if not self._checker.check_row(meta_table, row):
                stats.fail_check()
                continue
            insertion_result = self._output_driver.insert_row(row)
            if insertion_result is None:
                stats.fail_insert()
                continue
            stats.succeed_insert()
            table_db.append(row)
            self._checker.register_row(meta_table, row)
            yield row

    def _make_row(self, generators: GeneratorList) -> GeneratedRow:
        """Using the given list of generators, generate the row.
        Take driver interactivity into account.
        """
        row: GeneratedRow = {}
        for generator in generators:
            if not generator.is_database_generated or not self._output_driver.is_interactive:
                generated = generator.make_dict(self._database)
                row.update(generated)
        return row
