import json
from io import BytesIO
from typing import Tuple

import pytest
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float

from tests.fixtures.data_source import UserMockDataSource


@pytest.fixture
def mock_json_file() -> Tuple[BytesIO, str]:
    """Create JSON file io and filename."""
    obj = {
        'person': [
            {'name': 'Foo Bar', 'age': 12, 'nothing': None, 'flag': True},
            {'name': 'Bär Bar', 'age': 42.5, 'nothing': None, 'flag': False},
            {'name': 'Fóó Bar', 'age': -1, 'nothing': None, 'flag': True}
        ],
        'place': [
            {'country': None, 'city': 'Foo', 'index': 0.1, 'count': None},
            {'country': 'Bar', 'city': None, 'index': -12.44, 'count': 123},
            {'country': 'FooBar', 'city': None, 'index': None, 'count': 431}
        ],
        'number_test': [
            {'int1': 1, 'float1': None, 'float2': 3.14},
            {'int1': 2, 'float1': 2, 'float2': None},
            {'int1': None, 'float1': 3.14, 'float2': 1},
        ],
        'empty': []
    }
    json_bytes = json.dumps(obj).encode('utf-8')
    io = BytesIO(json_bytes)
    yield io, 'person_place.json'
    io.close()


@pytest.fixture
def mock_json_meta() -> MetaData:
    """Return meta for the mock JSON file."""
    meta = MetaData()
    Table(
        'person',
        meta,
        Column('name', String, nullable=False),
        Column('age', Float, nullable=False),
        Column('nothing', String, nullable=True),
        Column('flag', Boolean, nullable=False)
    )
    Table(
        'place',
        meta,
        Column('country', String, nullable=True),
        Column('city', String, nullable=True),
        Column('index', Float, nullable=True),
        Column('count', Integer, nullable=True)
    )
    Table(
        'number_test',
        meta,
        Column('int1', Integer, nullable=True),
        Column('float1', Float, nullable=True),
        Column('float2', Float, nullable=True)
    )
    Table(
        'empty',
        meta
    )
    return meta


@pytest.fixture
def user_mock_json(data_source_mock_maker, mock_json_file) -> UserMockDataSource:
    """Create a data source for the JSON mock file."""
    yield from data_source_mock_maker(*mock_json_file)
