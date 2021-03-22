from dataclasses import asdict
from itertools import cycle, islice

import pytest
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey

from core.facade.data_source import DataSourceFacade
from tests.fixtures.data_source import UserMockDataSource

CIRCULAR_TABLES = ('A', 'B', 'C')


@pytest.fixture(params=CIRCULAR_TABLES)
def circular_meta(request) -> MetaData:
    """Return circularly dependent tables.

    Tables A, B, C are created. The FKs are A->B, B->C, C->A.
    The parameter specifies which FK is nullable.
    """
    meta = MetaData()
    shift = 1
    tables_shifted = islice(cycle(CIRCULAR_TABLES), shift, len(CIRCULAR_TABLES) + shift)
    for table_name, next_table_name in zip(CIRCULAR_TABLES, tables_shifted):
        Table(
            table_name,
            meta,
            Column('pid', Integer, primary_key=True),
            Column('fid',
                   Integer,
                   ForeignKey('{}.pid'.format(next_table_name)),
                   nullable=table_name == request.param),
        )
    return meta


@pytest.fixture
def user_mock_circular_database(injector,
                                session,
                                user_project,
                                circular_meta) -> UserMockDataSource:
    facade = injector.get(DataSourceFacade)
    data_source = facade.create_mock_database(user_project.project.id,
                                              file_name='circular.db',
                                              mock_factory=lambda: circular_meta)
    session.commit()
    yield UserMockDataSource(
        data_source=data_source,
        **asdict(user_project)
    )
    facade.delete(data_source)
    session.flush()
