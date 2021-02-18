from typing import Iterator

from sqlalchemy import MetaData, select, Column

from core.model.data_source import DataSource
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.data_source.database_common import get_shared_connection, get_shared_engine
from core.service.data_source.identifier import Identifier
from core.service.exception import DataSourceIdentifierError


class DatabaseDataProvider(DataProvider):
    def __init__(self, data_source: DataSource, idf: Identifier):
        super().__init__(data_source, idf)
        self._column = self._get_column()

    def column_data(self) -> Iterator:
        conn = get_shared_connection(self._data_source)
        for row in conn.execute(select([self._column])):
            yield row[0]

    def _get_column(self) -> Column:
        engine = get_shared_engine(self._data_source)
        meta = MetaData()
        meta.reflect(bind=engine)
        if self._idf.table not in meta.tables:
            raise DataSourceIdentifierError('table not found', self._data_source, self._idf)
        table = meta.tables[self._idf.table]
        if self._idf.column not in table.columns:
            raise DataSourceIdentifierError('column not found', self._data_source, self._idf)
        return table.columns[self._idf.column]
