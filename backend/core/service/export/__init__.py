from core.model.data_source import DataSource
from core.service.column_generator import GeneratedDatabase
from core.service.export.table_generator import TableGenerator
from core.service.output_driver import MetaTableCounts, OutputDriver
from core.service.output_driver.database import DatabaseOutputDriver


class Export:
    def __init__(self, output_driver: OutputDriver):
        self._output_driver = output_driver

    def generate(self) -> GeneratedDatabase:
        for meta_table in self._output_driver.table_choices():
            generator = TableGenerator(meta_table, self._output_driver)
            while self._output_driver.expects_next_row():
                generator.insert_row()
        return self._output_driver.generated_database


class DatabaseExport(Export):
    def __init__(self, data_source: DataSource, meta_table_counts: MetaTableCounts):
        super().__init__(DatabaseOutputDriver(data_source, meta_table_counts))
