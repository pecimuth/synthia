from typing import Dict

from core.model.data_source import DataSource
from core.service.data_source.database import create_database_source_engine
from core.service.deserializer import StructureDeserializer
from core.service.generator import GeneratedDatabase
from core.service.generator.table_generator import TableGenerator


class DatabaseGenerator:

    def __init__(self, data_source: DataSource):
        self._data_source = data_source
        self._engine = create_database_source_engine(data_source)
        self._deserializer = StructureDeserializer(data_source.project)
        self._generated_database: GeneratedDatabase = {}
        self._generators = self._make_generators()

    def _make_generators(self) -> Dict[str,TableGenerator]:
        result = {}
        for meta_table in self._data_source.project.tables:
            generator = TableGenerator(meta_table, self._generated_database)
            result[meta_table.name] = generator
        return result

    def fill_database(self) -> GeneratedDatabase:
        meta_data = self._deserializer.deserialize()
        with self._engine.connect() as conn:
            self._generated_database.clear()
            for table in meta_data.sorted_tables:
                self._generators[table.name].fill_database(conn, table)
        return self._generated_database
