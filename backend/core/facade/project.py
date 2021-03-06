from typing import Optional, NewType

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
    def __init__(self, db_session: Session, user: User):
        self._db_session = db_session
        self._user = user

    def find_project(self, project_id: int) -> Project:
        return self._db_session.\
            query(Project). \
            filter(
                Project.id == project_id,
                Project.user == self._user
            ).\
            one()

    def generate_preview(self, project: Project, requisition: ExportRequisition) -> dict:
        preview_driver = PreviewOutputDriver()
        controller = ProcedureController(project, requisition, preview_driver)
        preview = controller.run()
        return preview.get_dict()

    def create_project(self, name: str) -> Project:
        project = Project(name=name, user=self._user)
        self._db_session.add(project)
        return project

    def generate_file_export(self,
                             project: Project,
                             requisition: ExportRequisition,
                             driver_name: str) -> FileOutputDriver:
        file_driver = FileOutputDriverFacade.make_driver(driver_name)
        controller = ProcedureController(project, requisition, file_driver)
        controller.run()
        return file_driver
