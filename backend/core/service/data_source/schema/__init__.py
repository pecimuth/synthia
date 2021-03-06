from typing import List, Iterable

from sqlalchemy.orm import Session

from core.model.data_source import DataSource
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.column_generator.assignment import GeneratorAssignment
from core.service.column_generator.base import ColumnGenerator
from core.service.column_generator.setting_facade import GeneratorSettingFacade
from core.service.data_source import DataSourceConstants
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.data_source.schema.csv_provider import CsvSchemaProvider
from core.service.data_source.schema.database_provider import DatabaseSchemaProvider
from core.service.data_source.schema.json_provider import JsonSchemaProvider
from core.service.exception import DataSourceError
from core.service.injector import Injector


class DataSourceSchemaImport:
    """Import schema from a data source, update the project structure,
    assign generators and estimate values in the new tables.
    """

    def __init__(self, project: Project, injector: Injector):
        self._project = project
        self._injector = injector

    def import_schema(self, data_source: DataSource, db_session: Session):
        """Import schema from the data source to the project.

        Tables are compared by name. If the table already exists, it is replaced.
        If it doesn't, it is added.
        Commits the current transaction, so that columns and constraints are properly bound.
        It may be possible to avoid this. However, it seems like the simplest solution.
        Generator assignment and parameter estimation is performed for the updated tables.
        """
        provider = self._create_schema_provider(data_source)
        new_tables = provider.read_structure()
        table_by_name = {
            table.name: table
            for table in self._project.tables
        }
        for imported_table in new_tables:
            if imported_table.name in table_by_name:
                db_session.delete(table_by_name[imported_table.name])
        db_session.flush()
        for imported_table in new_tables:
            imported_table.project = self._project
        db_session.commit()
        # generator assignment must come after commit
        # so that columns and constraints are properly bound
        generators = self._assign_generators(new_tables)
        self._estimate_all(generators)

    def _create_schema_provider(self, data_source: DataSource) -> SchemaProvider:
        if data_source.driver is not None:
            return DatabaseSchemaProvider(data_source, self._injector)
        elif data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
            return JsonSchemaProvider(data_source, self._injector)
        elif data_source.mime_type == DataSourceConstants.MIME_TYPE_CSV:
            return CsvSchemaProvider(data_source, self._injector)
        raise DataSourceError('no appropriate schema provider found', data_source)

    @classmethod
    def _assign_generators(cls, new_tables: List[MetaTable]) -> Iterable[ColumnGenerator]:
        for meta_table in new_tables:
            facade = GeneratorAssignment(meta_table)
            table_instances = facade.assign()
            yield from table_instances

    def _estimate_all(self, generators: Iterable[ColumnGenerator]):
        for column_gen in generators:
            facade = GeneratorSettingFacade(column_gen.setting)
            facade.estimate_params(column_gen, self._injector)
