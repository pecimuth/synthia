from typing import NewType

from sqlalchemy.orm import Session

from core.model.project import Project
from core.model.user import User
from core.service.generation_procedure.controller import ProcedureController
from core.service.generation_procedure.requisition import ExportRequisition
from core.service.output_driver import PreviewOutputDriver
from core.service.output_driver.file_driver.base import FileOutputDriver
from core.service.output_driver.file_driver.facade import FileOutputDriverFacade

ProjectStorage = NewType('ProjectStorage', str)


class ProjectFacade:
    """Provide CRUD operations related to Project."""

    def __init__(self, db_session: Session, user: User):
        self._db_session = db_session
        self._user = user

    def find_project(self, project_id: int) -> Project:
        """Find and return a project by its ID. Check that it belongs
        to the logged in user.
        """
        return self._db_session.\
            query(Project). \
            filter(
                Project.id == project_id,
                Project.user == self._user
            ).\
            one()

    @staticmethod
    def generate_preview(project: Project, requisition: ExportRequisition) -> dict:
        """Generate data for the project and return it as dict.

        Keys are table names, values are lists of dicts (GeneratedTable).
        """
        preview_driver = PreviewOutputDriver()
        controller = ProcedureController(project, requisition, preview_driver)
        preview = controller.run()
        return preview.get_dict()

    def create_project(self, name: str) -> Project:
        """Create and return a new project for the logged in user."""
        project = Project(name=name, user=self._user)
        self._db_session.add(project)
        return project

    @staticmethod
    def generate_file_export(project: Project,
                             requisition: ExportRequisition,
                             driver_name: str) -> FileOutputDriver:
        """Perform data generation with a file driver given by its name.
        Return the driver object.
        """
        file_driver = FileOutputDriverFacade.make_driver(driver_name)
        controller = ProcedureController(project, requisition, file_driver)
        controller.run()
        return file_driver
