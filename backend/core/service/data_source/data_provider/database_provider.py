from typing import Iterator, Tuple, Any, Optional

from sqlalchemy import MetaData, select, Column, func
from sqlalchemy.engine import Connection

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

    @property
    def _conn(self) -> Connection:
        return get_shared_connection(self._data_source)

    @property
    def _first_column(self) -> Column:
        return self._get_column(self._identifiers[0])

    def _select(self, identifiers: Identifiers) -> Iterator[Tuple]:
        columns = [self._get_column(idf) for idf in identifiers]
        for row in self._conn.execute(select(columns)):
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

    def scalar_data_not_none(self) -> Iterator[Any]:
        column = self._first_column
        query = select([column]).where(column.isnot(None))
        for row in self._conn.execute(query):
            yield row[0]

    def estimate_min(self) -> Any:
        column = self._first_column
        query = select([func.min(column)])
        return self._conn.execute(query).scalar()

    def estimate_max(self) -> Any:
        column = self._first_column
        query = select([func.max(column)])
        return self._conn.execute(query).scalar()

    def get_null_count(self) -> int:
        column = self._first_column
        query = select([func.count()]).where(column.is_(None))
        return self._conn.execute(query).scalar()

    def get_not_null_count(self) -> int:
        column = self._first_column
        query = select([func.count(column)])
        return self._conn.execute(query).scalar()

    def estimate_null_frequency(self) -> Optional[float]:
        null_count = self.get_null_count()
        not_null_count = self.get_not_null_count()
        count = null_count + not_null_count
        if count == 0:
            return None
        return null_count / count
