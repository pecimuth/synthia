from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.service.data_source import DataSourceConstants
from core.service.data_source.data_provider.database_provider import DatabaseDataProvider
from core.service.data_source.data_provider.json_provider import JsonDataProvider
from core.service.data_source.identifier import identifier_from_string
from core.service.exception import DataSourceError


def create_data_provider(meta_column: MetaColumn):
    data_source: DataSource = meta_column.data_source
    idf = identifier_from_string(meta_column.reflected_column_idf)
    if data_source.driver is not None:
        return DatabaseDataProvider(data_source, idf)
    elif data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
        return JsonDataProvider(data_source, idf)
    raise DataSourceError('no appropriate data provider', data_source)
