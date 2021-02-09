from typing import List, Union, Iterator

from sqlalchemy import create_engine, MetaData, select, Column
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL

from core.model.data_source import DataSource
from core.service.data_source import SourceDataProvider


def create_database_source_engine(data_source: DataSource) -> Engine:
    url = URL(
        drivername=data_source.driver,
        username=data_source.usr,
        password=data_source.pwd,
        host=data_source.host,
        port=data_source.port,
        database=data_source.db
    )
    print(url)
    return create_engine(url)


class DatabaseSourceProvider(SourceDataProvider):

    def __init__(self, data_source: DataSource, idf: Union[str, None]):
        super().__init__(data_source, idf)
        self._engine = create_database_source_engine(data_source)
        self._column = self._get_column()

    def test_connection(self) -> bool:
        return True

    def identifiers(self) -> List[str]:
        meta = MetaData()
        meta.reflect(bind=self._engine)
        identifiers = []
        for tab in meta.tables.values():
            for col in tab.c.values():
                idf = '{}.{}'.format(tab.name, col.name)
                identifiers.append(idf)
        return identifiers

    def column_data(self) -> Iterator:
        with self._engine.connect() as conn:
            yield from select([self._column]).as_scalar()

    def _get_column(self) -> Column:
        if self._idf is None:
            raise Exception('identifier is mandatory')
        if '.' not in self._idf:
            raise Exception('bad identifier format: {}'.format(self._idf))
        tab_name, col_name = self._idf.split('.', 2)
        meta = MetaData()
        meta.reflect(bind=self._engine)
        if tab_name not in meta.tables:
            raise Exception('table {} not found in the schema'.format(tab_name))
        table = meta.tables[tab_name]
        if col_name not in table.columns:
            raise Exception('column {}.{} not found in the schema'.format(tab_name, col_name))
        return table.columns[col_name]
