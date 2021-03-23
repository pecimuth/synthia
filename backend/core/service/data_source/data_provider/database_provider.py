from typing import Iterator, Tuple, Any, Optional

from sqlalchemy import MetaData, select, Column, func
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.data_source.database_common import DatabaseConnectionManager
from core.service.data_source.identifier import Identifiers, Identifier
from core.service.exception import DataSourceIdentifierError, DatabaseNotReadable, FatalDatabaseError


class DatabaseDataProvider(DataProvider):
    """Provide data from a database."""

    def scalar_data(self) -> Iterator[Any]:
        idf = self._identifiers[0]
        for tup in self._select([idf]):
            yield tup[0]

    def vector_data(self) -> Iterator[Tuple]:
        for tup in self._select(self._identifiers):
            yield tup

    @property
    def _conn(self) -> Connection:
        """Return database connection."""
        conn_manager = self._injector.get(DatabaseConnectionManager)
        return conn_manager.get_connection(self._data_source)

    @property
    def _first_column(self) -> Column:
        """Return column (bound to a DB connection) identified by the first identifier."""
        return self._get_column(self._identifiers[0])

    def _safe_exec(self, *args, **kwargs):
        """Execute statement and convert SQLAlchemy exception
        to FatalDatabaseError so that it can be caught by our handlers."""
        try:
            return self._conn.execute(*args, **kwargs)
        except SQLAlchemyError:
            raise FatalDatabaseError()

    def _select(self, identifiers: Identifiers) -> Iterator[Tuple]:
        """Yield tuples of values  selected by identifiers."""
        columns = [self._get_column(idf) for idf in identifiers]
        for row in self._safe_exec(select(columns)):
            yield row

    def _get_column(self, idf: Identifier) -> Column:
        """Convert identifier to a column bound to a database connection."""
        conn_manager = self._injector.get(DatabaseConnectionManager)
        engine = conn_manager.get_engine(self._data_source)
        meta = MetaData()
        try:
            meta.reflect(bind=engine)
        except SQLAlchemyError:
            raise DatabaseNotReadable(self._data_source)
        if idf.table not in meta.tables:
            raise DataSourceIdentifierError('Table not found', self._data_source, repr(idf))
        table = meta.tables[idf.table]
        if idf.column not in table.columns:
            raise DataSourceIdentifierError('Column not found', self._data_source, repr(idf))
        return table.columns[idf.column]

    def scalar_data_not_none(self) -> Iterator[Any]:
        column = self._first_column
        query = select([column]).where(column.isnot(None))
        for row in self._safe_exec(query):
            yield row[0]

    def estimate_min(self) -> Any:
        column = self._first_column
        query = select([func.min(column)])
        return self._safe_exec(query).scalar()

    def estimate_max(self) -> Any:
        column = self._first_column
        query = select([func.max(column)])
        return self._safe_exec(query).scalar()

    def get_null_count(self) -> int:
        column = self._first_column
        query = select([func.count()]).where(column.is_(None))
        return self._safe_exec(query).scalar()

    def get_not_null_count(self) -> int:
        column = self._first_column
        query = select([func.count(column)])
        return self._safe_exec(query).scalar()

    def estimate_null_frequency(self) -> Optional[float]:
        null_count = self.get_null_count()
        not_null_count = self.get_not_null_count()
        count = null_count + not_null_count
        if count == 0:
            return None
        return null_count / count

    def estimate_mean(self) -> Optional[float]:
        column = self._first_column
        query = select([func.avg(column)])
        return self._safe_exec(query).scalar()

    def estimate_variance(self) -> Optional[float]:
        column = self._first_column
        query = select([
            func.avg(column),
            func.avg(column * column)
        ])
        avg, square_avg = self._safe_exec(query).fetchone()
        if avg is None:
            return None
        return max(square_avg - avg ** 2, 0)
