from typing import Iterable, Tuple, Union

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.column_generator.setting_facade import GeneratorSettingFacade, GeneratorList
from core.service.deserializer import StructureDeserializer
from core.service.exception import SomeError
from core.service.generation_procedure.constraint_checker import ConstraintChecker
from core.service.generation_procedure.database import GeneratedRow, GeneratedDatabase
from core.service.generation_procedure.requisition import ExportRequisition
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
        self._database: Union[GeneratedDatabase, None] = None

    def run(self) -> GeneratedDatabase:
        self._database = GeneratedDatabase()
        self._output_driver.start_run()
        for table, meta_table in self._sorted_tables():
            self._output_driver.switch_table(table, meta_table)
            try:
                self._table_loop(meta_table)
            except SomeError:
                # TODO log
                pass
        self._output_driver.end_run(self._database)
        return self._database

    def _sorted_tables(self) -> Iterable[Tuple[Table, MetaTable]]:
        meta_table_by_name = {
            table.name: table
            for table in self._project.tables
        }
        deserializer = StructureDeserializer(self._project)
        meta = deserializer.deserialize()
        for table in meta.sorted_tables:
            if table.name not in self._requisition:
                continue
            yield table, meta_table_by_name[table.name]

    def _table_loop(self, meta_table: MetaTable):
        table_db = self._database.add_table(meta_table.name)
        stats = self._statistics.get_table_statistics(meta_table.name)
        generators = GeneratorSettingFacade.instances_from_table(meta_table)
        checker = ConstraintChecker(meta_table, self._database, self._output_driver.is_interactive)
        while stats.expects_next_row:
            row = self._make_row(generators)
            if not checker.check_row(row):
                stats.fail_check()
                continue
            insertion_result = self._output_driver.insert_row(row)
            if insertion_result is None:
                stats.fail_insert()
                continue
            stats.succeed_insert()
            table_db.append(row)
            checker.register_row(row)

    def _make_row(self, generators: GeneratorList) -> GeneratedRow:
        row: GeneratedRow = {}
        for generator in generators:
            if not generator.is_database_generated or not self._output_driver.is_interactive:
                generated = generator.make_dict(self._database)
                row.update(generated)
        return row
