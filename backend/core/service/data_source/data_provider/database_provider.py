from typing import Iterator

from sqlalchemy import MetaData, select, Column

from core.model.data_source import DataSource
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.data_source.database_common import create_database_source_engine
from core.service.data_source.identifier import Identifier
from core.service.exception import DataSourceIdentifierError


class DatabaseDataProvider(DataProvider):
    def __init__(self, data_source: DataSource, idf: Identifier):
        super().__init__(data_source, idf)
        self._engine = create_database_source_engine(data_source)
        self._column = self._get_column()

    def column_data(self) -> Iterator:
        # TODO is this necessary?
        with self._engine.connect():
            yield from select([self._column]).as_scalar()

    def _get_column(self) -> Column:
        meta = MetaData()
        meta.reflect(bind=self._engine)
        if self._idf.table not in meta.tables:
            raise DataSourceIdentifierError('table not found', self._data_source, self._idf)
        table = meta.tables[self._idf.table]
        if self._idf.column not in table.columns:
            raise DataSourceIdentifierError('column not found', self._data_source, self._idf)
        return table.columns[self._idf.column]
