from typing import List

from core.model.data_source import DataSource
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.data_source.schema.database_provider import DatabaseSchemaProvider
from core.service.data_source.schema.json_provider import JsonSchemaProvider


def create_schema_provider(data_source: DataSource) -> SchemaProvider:
    if data_source.driver is not None:
        return DatabaseSchemaProvider(data_source)
    if data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
        return JsonSchemaProvider(data_source)
    raise Exception('no appropriate schema provider found')


def update_project_schema(proj: Project, schema: List[MetaTable]):
    for table in schema:
        table.project = proj
