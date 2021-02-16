from core.model.meta_column import MetaColumn
from core.service.data_source.data_provider.database_provider import DatabaseDataProvider
from core.service.data_source.identifier import identifier_from_string


def create_data_provider(meta_column: MetaColumn):
    data_source = meta_column.data_source
    idf = identifier_from_string(meta_column.reflected_column_idf)
    if data_source.driver is not None:
        return DatabaseDataProvider(data_source, idf)
    raise Exception('no appropriate data provider found')
