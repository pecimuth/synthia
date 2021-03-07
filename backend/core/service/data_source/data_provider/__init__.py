from typing import List
from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.service.data_source import DataSourceConstants
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.data_source.data_provider.csv_provider import CsvDataProvider
from core.service.data_source.data_provider.database_provider import DatabaseDataProvider
from core.service.data_source.data_provider.json_provider import JsonDataProvider
from core.service.data_source.identifier import Identifiers, identifier_from_string
from core.service.exception import DataSourceError, SomeError
from core.service.injector import Injector


class DataProviderFactory:
    def __init__(self, meta_columns: List[MetaColumn], injector: Injector):
        self._meta_columns = meta_columns
        self._injector = injector

    def find_provider(self):
        data_source = self._single_data_source()
        identifiers = self._make_identifiers()
        return self._create_data_provider(data_source, identifiers)

    def _create_data_provider(self, data_source: DataSource, identifiers: Identifiers) -> DataProvider:
        if data_source.driver is not None:
            return DatabaseDataProvider(data_source, identifiers, self._injector)
        elif data_source.mime_type == DataSourceConstants.MIME_TYPE_JSON:
            return JsonDataProvider(data_source, identifiers, self._injector)
        elif data_source.mime_type == DataSourceConstants.MIME_TYPE_CSV:
            return CsvDataProvider(data_source, identifiers, self._injector)
        raise DataSourceError('no appropriate data provider', data_source)

    def _single_data_source(self) -> DataSource:
        data_source = None
        for meta_column in self._meta_columns:
            if data_source is None:
                data_source = meta_column.data_source
            elif data_source is not meta_column.data_source:
                raise SomeError('mixed data sources are not supported')
        if data_source is None:
            raise SomeError('the column list provides no data source')
        return data_source

    def _make_identifiers(self) -> Identifiers:
        identifier_list = []
        for meta_column in self._meta_columns:
            idf_string = meta_column.reflected_column_idf
            idf = identifier_from_string(idf_string)
            identifier_list.append(idf)
        return identifier_list
