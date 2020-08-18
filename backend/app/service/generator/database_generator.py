from typing import Dict

from app.model.project import Project
from app.service.deserializer import StructureDeserializer
from app.service.extern_db import ExternDb
from app.service.generator import GeneratedDatabase
from app.service.generator.table_generator import TableGenerator


class DatabaseGenerator:

    def __init__(self, proj: Project):
        self._proj = proj
        self._deserializer = StructureDeserializer(proj)
        self._extern_db = ExternDb(proj)
        self._generated_database: GeneratedDatabase = {}
        self._generators = self._make_generators()

    def _make_generators(self) -> Dict[str,TableGenerator]:
        result = {}
        for meta_table in self._proj.tables:
            generator = TableGenerator(meta_table, self._generated_database)
            result[meta_table.name] = generator
        return result

    def fill_database(self) -> GeneratedDatabase:
        meta_data = self._deserializer.deserialize()
        conn = self._extern_db.engine.connect()
        self._generated_database.clear()
        for table in meta_data.sorted_tables:
            self._generators[table.name].fill_database(conn, table)
        conn.close()
        return self._generated_database
