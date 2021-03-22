from dataclasses import dataclass

import pytest

from core.facade.project import ProjectFacade
from core.model.project import Project
from core.model.user import User


@dataclass
class UserProject:
    user: User
    project: Project


PROJECT_NAME = 'My Test Project'


@pytest.fixture
def user_project(injector, session, user) -> UserProject:
    facade = injector.get(ProjectFacade)
    project = facade.create_project(PROJECT_NAME)
    session.commit()
    yield UserProject(
        user=user,
        project=project
    )
    if session.is_active:
        session.delete(project)
