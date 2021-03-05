import os

from sqlalchemy.orm import Session

from core.model.data_source import DataSource
from core.model.user import User
from core.service.data_source.schema import DataSourceSchemaImport
from core.service.exception import DataSourceError
from core.service.generation_procedure.controller import ProcedureController
from core.service.generation_procedure.requisition import ExportRequisition
from core.service.output_driver.database import DatabaseOutputDriver


class DataSourceFacade:
    def __init__(self, db_session: Session, user: User):
        self._db_session = db_session
        self._user = user

    @staticmethod
    def export_to_data_source(data_source: DataSource, requisition: ExportRequisition):
        if data_source.driver is None:
            return DataSourceError('The data source is not a database', data_source)
        database_driver = DatabaseOutputDriver(data_source)
        controller = ProcedureController(data_source.project, requisition, database_driver)
        controller.run()

    def import_schema(self, data_source: DataSource):
        schema_import = DataSourceSchemaImport(data_source.project)
        schema_import.import_schema(data_source, self._db_session)

    def delete(self, data_source: DataSource):
        if data_source.file_path is not None:
            try:
                os.remove(data_source.file_path)
            except OSError:
                pass
        self._db_session.delete(data_source)

    @staticmethod
    def read_file_content(data_source: DataSource) -> bytes:
        if data_source.file_path is None:
            raise DataSourceError('Data source has no file', data_source)
        try:
            with open(data_source.file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            raise DataSourceError('File not found', data_source)
