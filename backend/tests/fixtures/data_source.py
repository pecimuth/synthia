from dataclasses import dataclass, asdict
from io import BytesIO
from typing import Callable

import pytest

from core.facade.data_source import DataSourceFacade
from core.model.data_source import DataSource
from tests.fixtures.project import UserProject


@dataclass
class UserMockDataSource(UserProject):
    """User, their project and its data source."""
    data_source: DataSource


@pytest.fixture
def user_mock_database(injector, session, user_project) -> UserMockDataSource:
    """Create mock database in the user's project."""
    facade = injector.get(DataSourceFacade)
    data_source = facade.create_mock_database(user_project.project.id)
    session.commit()
    yield UserMockDataSource(
        data_source=data_source,
        **asdict(user_project)
    )
    if session.is_active:
        facade.delete(data_source)


@pytest.fixture
def data_source_mock_maker(injector, session, user_project) -> Callable[[BytesIO, str], UserMockDataSource]:
    """Return a callable, that takes file content and file name and creates
    a data source in the user's project."""
    def maker(file_content: BytesIO, file_name: str) -> UserMockDataSource:
        facade = injector.get(DataSourceFacade)
        data_source = facade.create_data_source_for_file(user_project.project.id, file_name)
        with open(data_source.file_path, 'wb') as file:
            file.write(file_content.read())
        session.commit()
        yield UserMockDataSource(
            data_source=data_source,
            **asdict(user_project)
        )
        facade.delete(data_source)
        session.flush()
    return maker
