from core.model.meta_column import MetaColumn
from core.service.data_source.data_provider.database_provider import DatabaseDataProvider


def create_data_provider(meta_column: MetaColumn):
    data_source = meta_column.data_source
    idf = meta_column.reflected_column_idf
    if data_source.driver is not None:
        return DatabaseDataProvider(data_source, idf)
    raise Exception('no appropriate data provider found')
