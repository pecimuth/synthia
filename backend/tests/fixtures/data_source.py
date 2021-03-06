from dataclasses import dataclass, asdict

import pytest

from core.facade.data_source import DataSourceFacade
from core.model.data_source import DataSource
from tests.fixtures.project import UserProject


@dataclass
class UserMockDatabase(UserProject):
    data_source: DataSource


@pytest.fixture
def user_mock_database(injector, session, user_project) -> UserProject:
    facade = injector.get(DataSourceFacade)
    data_source = facade.create_mock_database(user_project.project.id)
    session.commit()
    yield UserMockDatabase(
        data_source=data_source,
        **asdict(user_project)
    )
    session.delete(data_source)
    session.flush()
