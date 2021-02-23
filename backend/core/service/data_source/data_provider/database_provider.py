from typing import Iterator, Tuple, Any

from sqlalchemy import MetaData, select, Column

from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.data_source.database_common import get_shared_connection, get_shared_engine
from core.service.data_source.identifier import Identifiers, Identifier
from core.service.exception import DataSourceIdentifierError


class DatabaseDataProvider(DataProvider):
    def scalar_data(self) -> Iterator[Any]:
        idf = self._identifiers[0]
        for tup in self._select([idf]):
            yield tup[0]

    def vector_data(self) -> Iterator[Tuple]:
        for tup in self._select(self._identifiers):
            yield tup

    def _select(self, identifiers: Identifiers) -> Iterator[Tuple]:
        columns = [self._get_column(idf) for idf in identifiers]
        conn = get_shared_connection(self._data_source)
        for row in conn.execute(select(columns)):
            yield row

    def _get_column(self, idf: Identifier) -> Column:
        engine = get_shared_engine(self._data_source)
        meta = MetaData()
        meta.reflect(bind=engine)
        if idf.table not in meta.tables:
            raise DataSourceIdentifierError('table not found', self._data_source, idf)
        table = meta.tables[idf.table]
        if idf.column not in table.columns:
            raise DataSourceIdentifierError('column not found', self._data_source, idf)
        return table.columns[idf.column]
