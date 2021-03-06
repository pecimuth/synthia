from dataclasses import dataclass

import pytest

from core.facade.project import ProjectFacade
from core.model.project import Project
from core.model.user import User


@dataclass
class ProjectUser:
    user: User
    project: Project


PROJECT_NAME = 'My Test Project'


@pytest.fixture
def project(injector, session, user) -> ProjectUser:
    facade = injector.get(ProjectFacade)
    project = facade.create_project(PROJECT_NAME)
    session.commit()
    yield ProjectUser(
        user=user,
        project=project
    )
    session.delete(project)
    session.commit()
