from core.model.data_source import DataSource
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.data_source.schema.database_provider import DatabaseSchemaProvider
from core.service.data_source.schema.json_provider import JsonSchemaProvider
from core.service.exception import DataSourceError


class DataSourceSchemaImport:
    def __init__(self, project: Project):
        self._project = project
        self._table_by_name = {
            table.name: table
            for table in self._project.tables
        }

    def import_schema(self, data_source: DataSource):
        provider = self._create_schema_provider(data_source)
        new_tables = provider.read_structure()
        for new_table in new_tables:
            if new_table.name in self._table_by_name:
                self._add_missing_columns(
                    self._table_by_name[new_table.name],
                    new_table
                )
            else:
                new_table.project = self._project

    @classmethod
    def _create_schema_provider(cls, data_source: DataSource) -> SchemaProvider:
        if data_source.driver is not None:
            return DatabaseSchemaProvider(data_source)
        if data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
            return JsonSchemaProvider(data_source)
        raise DataSourceError('no appropriate schema provider found', data_source)

    @classmethod
    def _add_missing_columns(cls, project_table: MetaTable, imported_table: MetaTable):
        col_by_name = {
            col.name: col
            for col in project_table.columns
        }
        for col in imported_table.columns:
            if col.name not in col_by_name:
                col.table = project_table
