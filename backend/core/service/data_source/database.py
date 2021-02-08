from typing import List, Union, Iterator

from sqlalchemy import create_engine, MetaData, Table, select, Column

from core.model.data_source import DataSource
from core.service.data_source import SourceDataProvider


class DatabaseSourceProvider(SourceDataProvider):

    def __init__(self, data_source: DataSource):
        super().__init__(data_source)
        self._engine = create_engine(data_source.connection_string)

    def test_connection(self) -> bool:
        return True

    def get_identifiers(self) -> List[str]:
        meta = MetaData()
        meta.reflect(bind=self._engine)
        identifiers = []
        for tab in meta.tables.values():
            for col in tab.c.values():
                idf = '{}.{}'.format(tab.name, col.name)
                identifiers.append(idf)
        return identifiers

    def get_data(self, identifier: Union[str, None] ) -> Iterator:
        if identifier is None:
            raise Exception('identifier is mandatory')
        column = self._get_column(identifier)
        with self._engine.connect() as conn:
            yield from select([column]).as_scalar()

    def _get_column(self, identifier: str) -> Column:
        if '.' not in identifier:
            raise Exception('bad identifier format: {}'.format(identifier))
        tab_name, col_name = identifier.split('.', 2)
        meta = MetaData()
        meta.reflect(bind=self._engine)
        if tab_name not in meta.tables:
            raise Exception('table {} not found in the schema'.format(tab_name))
        table = meta.tables[tab_name]
        if col_name not in table.columns:
            raise Exception('column {}.{} not found in the schema'.format(tab_name, col_name))
        return table.columns[col_name]
