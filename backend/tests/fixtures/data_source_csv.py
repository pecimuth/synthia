from io import BytesIO
from typing import Tuple

import pytest
from sqlalchemy import MetaData, Table, Column, String, Float

from tests.fixtures.data_source import UserMockDataSource


@pytest.fixture
def mock_csv_file() -> Tuple[BytesIO, str]:
    """Create CSV io and file name."""
    content = '''"title","length","year_released","box_office"
"Something Something",123,2019,
"Test",99,2023,"$333"
"Wow",12,2021,"$9"
'''
    io = BytesIO(content.encode('utf-8'))
    yield io, 'movie.csv'
    io.close()


@pytest.fixture
def mock_csv_meta() -> MetaData:
    """Return the meta for the mock CSV file."""
    meta = MetaData()
    Table(
        'movie',
        meta,
        Column('title', String, nullable=False),
        Column('length', Float, nullable=False),
        Column('year_released', Float, nullable=False),
        Column('box_office', String, nullable=False)
    )
    return meta


@pytest.fixture
def user_mock_csv(data_source_mock_maker, mock_csv_file) -> UserMockDataSource:
    """Create a data source for the mock CSV file."""
    yield from data_source_mock_maker(*mock_csv_file)
