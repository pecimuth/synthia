from sqlalchemy.orm import Session

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.data_source.schema.database_provider import DatabaseSchemaProvider
from core.service.data_source.schema.json_provider import JsonSchemaProvider
from core.service.exception import DataSourceError


class DataSourceSchemaImport:
    def __init__(self, project: Project):
        self._project = project

    def import_schema(self, data_source: DataSource, db_session: Session):
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

    @classmethod
    def _create_schema_provider(cls, data_source: DataSource) -> SchemaProvider:
        if data_source.driver is not None:
            return DatabaseSchemaProvider(data_source)
        if data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
            return JsonSchemaProvider(data_source)
        raise DataSourceError('no appropriate schema provider found', data_source)
