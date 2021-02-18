from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
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
        for imported_table in new_tables:
            if imported_table.name in self._table_by_name:
                project_table = self._table_by_name[imported_table.name]
                project_table.data_source = data_source
                self._update_columns(project_table, imported_table)
            else:
                imported_table.project = self._project

    @classmethod
    def _create_schema_provider(cls, data_source: DataSource) -> SchemaProvider:
        if data_source.driver is not None:
            return DatabaseSchemaProvider(data_source)
        if data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
            return JsonSchemaProvider(data_source)
        raise DataSourceError('no appropriate schema provider found', data_source)

    @classmethod
    def _update_columns(cls, project_table: MetaTable, imported_table: MetaTable):
        col_by_name = {
            col.name: col
            for col in project_table.columns
        }
        for imported_col in imported_table.columns:
            if imported_col.name in col_by_name:
                project_col: MetaColumn = col_by_name[imported_col.name]
                cls._update_column(project_col, imported_col)
            else:
                imported_col.table = project_table

    @classmethod
    def _update_column(cls, project_col: MetaColumn, imported_col: MetaColumn):
        overwrite_attrs = [
            'col_type',
            'nullable',
            'generator_name',
            'generator_params',
            'data_source',
            'reflected_column_idf'
        ]
        for attr in overwrite_attrs:
            new_value = getattr(imported_col, attr)
            setattr(project_col, attr, new_value)
