import os
from typing import Callable

from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from core.facade.project import ProjectFacade, ProjectStorage
from core.model.data_source import DataSource
from core.model.project import Project
from core.model.user import User
from core.service.data_source.database_common import DatabaseConnectionManager
from core.service.data_source.file_common import FileDataSourceFactory, is_file_allowed
from core.service.data_source.schema import DataSourceSchemaImport
from core.service.exception import DataSourceError, FileNotAllowedError
from core.service.generation_procedure.controller import ProcedureController
from core.service.generation_procedure.requisition import ExportRequisition
from core.service.injector import Injector
from core.service.mock_schema import mock_book_author_publisher
from core.service.output_driver.database import DatabaseOutputDriver


class DataSourceFacade:
    """Provide CRUD operations related to DataSource."""

    def __init__(self,
                 db_session: Session,
                 user: User,
                 injector: Injector,
                 project_storage: ProjectStorage,
                 conn_manager: DatabaseConnectionManager,
                 project_facade: ProjectFacade):
        self._db_session = db_session
        self._user = user
        self._injector = injector
        self._project_storage = project_storage
        self._conn_manager = conn_manager
        self._project_facade = project_facade

    def find_data_source(self, data_source_id: int) -> DataSource:
        """Find and return a data source by ID. Check that it belongs
        to the logged in user."""
        return self._db_session.query(DataSource).\
            join(DataSource.project).\
            filter(
                DataSource.id == data_source_id,
                Project.user == self._user
            ).\
            one()

    def export_to_data_source(self, data_source: DataSource, requisition: ExportRequisition):
        """Generate the data a INSERT them to the data source.

        The data source must be a database.
        """
        if data_source.driver is None:
            return DataSourceError('The data source is not a database', data_source)
        database_driver = DatabaseOutputDriver(data_source, self._conn_manager)
        controller = ProcedureController(data_source.project, requisition, database_driver)
        controller.run()

    def import_schema(self, data_source: DataSource):
        """Import schema from a data source to its project."""
        schema_import = DataSourceSchemaImport(data_source.project, self._injector)
        schema_import.import_schema(data_source, self._db_session)

    def delete(self, data_source: DataSource):
        """Delete a data source and its related file, in case it exists."""
        if data_source.file_path is not None:
            try:
                os.remove(data_source.file_path)
            except OSError:
                pass
        self._db_session.delete(data_source)

    @staticmethod
    def read_file_content(data_source: DataSource) -> bytes:
        """Read the bytes from the data source's files."""
        if data_source.file_path is None:
            raise DataSourceError('Data source has no file', data_source)
        try:
            with open(data_source.file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            raise DataSourceError('File not found', data_source)

    def create_mock_database(self,
                             project_id: int,
                             file_name: str = 'books.db',
                             mock_factory: Callable[[], MetaData] = lambda: mock_book_author_publisher()
                             ) -> DataSource:
        """Create an SQLite database in the project. Create the database schema.
        Create and return a data source representing the database.
        """
        if not is_file_allowed(file_name):
            raise FileNotAllowedError()
        project = self._project_facade.find_project(project_id)
        # create and flush the data source (conn_manager needs the id)
        factory = FileDataSourceFactory(project, file_name, self._project_storage)
        data_source = factory.create_data_source()
        self._db_session.add(data_source)
        self._db_session.flush()
        # create the sqlite file
        try:
            with open(factory.file_path, 'w'):
                pass
        except OSError:
            raise DataSourceError('The file could not be saved', data_source)
        # create the schema
        engine = self._conn_manager.get_engine(data_source)
        mock_meta = mock_factory()
        mock_meta.bind = engine
        mock_meta.create_all()
        return data_source

    def create_data_source_for_file(self, project_id: int, file_name: str) -> DataSource:
        """Create and return a data source to be used with a file.

        The file may be created after the call in the assigned file path.
        """
        if not is_file_allowed(file_name):
            raise FileNotAllowedError()
        project = self._project_facade.find_project(project_id)
        factory = FileDataSourceFactory(project, file_name, self._project_storage)
        data_source = factory.create_data_source()
        self._db_session.add(data_source)
        return data_source
