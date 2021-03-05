from typing import Optional

from sqlalchemy.orm import Session

from core.model.project import Project
from core.model.user import User
from core.service.generation_procedure.controller import ProcedureController
from core.service.generation_procedure.requisition import ExportRequisition
from core.service.output_driver import PreviewOutputDriver
from core.service.output_driver.file_driver.base import FileOutputDriver
from core.service.output_driver.file_driver.facade import FileOutputDriverFacade


class ProjectFacade:
    def __init__(self, db_session: Session, user: User):
        self._db_session = db_session
        self._user = user
        self._project: Optional[Project] = None

    def find_project(self, project_id: int) -> Project:
        self._project = self._db_session.\
            query(Project). \
            filter(
                Project.id == project_id,
                Project.user == self._user
            ).\
            one()
        return self._project

    def generate_preview(self, requisition: ExportRequisition) -> dict:
        preview_driver = PreviewOutputDriver()
        controller = ProcedureController(self._project, requisition, preview_driver)
        preview = controller.run()
        return preview.get_dict()

    def create_project(self, name: str) -> Project:
        project = Project(name=name, user=self._user)
        self._db_session.add(project)
        return project

    def generate_file_export(self,
                             requisition: ExportRequisition,
                             driver_name: str) -> FileOutputDriver:
        file_driver = FileOutputDriverFacade.make_driver(driver_name)
        controller = ProcedureController(self._project, requisition, file_driver)
        controller.run()
        return file_driver
