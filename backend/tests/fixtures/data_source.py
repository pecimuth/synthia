import json
from dataclasses import dataclass, asdict
from io import BytesIO
from typing import Tuple

import pytest
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean, Float

from core.facade.data_source import DataSourceFacade
from core.model.data_source import DataSource
from tests.fixtures.project import UserProject


@dataclass
class UserMockDatabase(UserProject):
    data_source: DataSource


@pytest.fixture
def user_mock_database(injector, session, user_project) -> UserMockDatabase:
    facade = injector.get(DataSourceFacade)
    data_source = facade.create_mock_database(user_project.project.id)
    session.commit()
    yield UserMockDatabase(
        data_source=data_source,
        **asdict(user_project)
    )
    facade.delete(data_source)
    session.flush()


@pytest.fixture
def mock_json_file() -> Tuple[BytesIO, str]:
    obj = {
        'person': [
            {'name': 'Foo Bar', 'age': 12, 'nothing': None, 'flag': True},
            {'name': 'Bär Bar', 'age': 42, 'nothing': None, 'flag': False},
            {'name': 'Fóó Bar', 'age': -1, 'nothing': None, 'flag': True}
        ],
        'place': [
            {'country': None, 'city': 'Foo', 'index': 0.1, 'count': None},
            {'country': 'Bar', 'city': None, 'index': -12.44, 'count': 123},
            {'country': 'FooBar', 'city': None, 'index': None, 'count': 431}
        ]
    }
    json_bytes = json.dumps(obj).encode('utf-8')
    io = BytesIO(json_bytes)
    yield io, 'person_place.json'
    io.close()


@pytest.fixture
def mock_json_meta() -> MetaData:
    meta = MetaData()
    Table(
        'person',
        meta,
        Column('name', String, nullable=False),
        Column('age', Integer, nullable=False),
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
    return meta


@dataclass
class UserMockJson(UserProject):
    data_source: DataSource


@pytest.fixture
def user_mock_json(injector, session, user_project, mock_json_file) -> UserMockJson:
    facade = injector.get(DataSourceFacade)
    file_content, file_name = mock_json_file
    data_source = facade.create_data_source_for_file(user_project.project.id, file_name)
    with open(data_source.file_path, 'wb') as file:
        file.write(file_content.read())
    session.commit()
    yield UserMockJson(
        data_source=data_source,
        **asdict(user_project)
    )
    facade.delete(data_source)
    session.flush()
