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
from core.service.data_source.schema.database_provider import DatabaseSchemaProvider
from core.service.data_source.schema.json_provider import JsonSchemaProvider
from core.service.exception import DataSourceError
from core.service.injector import Injector


class DataSourceSchemaImport:
    def __init__(self, project: Project, injector: Injector):
        self._project = project
        self._injector = injector

    def import_schema(self, data_source: DataSource, db_session: Session):
        provider = self._create_schema_provider(data_source)
        new_tables = provider.read_structure()
        generators = self._assign_generators(new_tables)
        self._estimate_all(generators)
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

    def _create_schema_provider(self, data_source: DataSource) -> SchemaProvider:
        if data_source.driver is not None:
            return DatabaseSchemaProvider(data_source, self._injector)
        if data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
            return JsonSchemaProvider(data_source, self._injector)
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
