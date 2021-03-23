import json
import os
import tempfile
from dataclasses import dataclass, asdict
from io import BytesIO
from typing import Callable, AnyStr, Tuple

import pytest

from core.facade.data_source import DataSourceFacade
from core.model.data_source import DataSource
from core.model.project import Project
from core.service.types import json_serialize_default
from tests.fixtures.project import UserProject
from web.view.project import SaveView


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
def user_import_mock_database(injector, session, user_mock_database) -> UserMockDataSource:
    """Return the mock database data source and import its schema
    to the user's project."""
    facade = injector.get(DataSourceFacade)
    facade.import_schema(user_mock_database.data_source)
    session.commit()
    return user_mock_database


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


@pytest.fixture(params=[(7, 11)])
def saved_mock_project_file(request, session, user_import_mock_database) -> Tuple[int, AnyStr]:
    """Save project with imported mock database to a file
    and return the file descriptor and path."""
    fd, file_path = tempfile.mkstemp()
    # we need to query the project again
    # for some reason direct usage of user_import_mock_database.project fails
    project = session.query(Project).\
        filter(Project.id == user_import_mock_database.project.id).\
        one()
    py_dump = SaveView().dump({
        'project': project,
        'requisition': {
            'rows': [
                {
                    'table_name': meta_table.name,
                    'row_count': request.param[0],
                    'seed': request.param[1]
                }
                for meta_table in project.tables
            ]
        }
    })
    json_dump = json.dumps(py_dump, indent=2, default=json_serialize_default)
    os.write(fd, json_dump.encode('utf-8'))
    yield fd, file_path
    os.close(fd)
    os.unlink(file_path)
