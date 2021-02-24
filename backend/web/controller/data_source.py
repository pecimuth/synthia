import functools
import os

from flasgger import swag_from
from flask import Blueprint, request, current_app
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from core.model.data_source import DataSource
from core.service.data_source import DataSourceConstants
from core.service.data_source.database_common import DatabaseConnectionManager
from core.service.data_source.file_common import FileDataSourceFactory, is_file_allowed
from core.service.data_source.schema import DataSourceSchemaImport
from core.service.deserializer import create_mock_meta
from core.service.generation_procedure.controller import ProcedureController
from core.service.output_driver.database import DatabaseOutputDriver
from web.controller.auth import login_required
from web.controller.util import BAD_REQUEST_SCHEMA, bad_request, find_user_project, PROJECT_NOT_FOUND, INVALID_INPUT, \
    DATA_SOURCE_NOT_FOUND, ok_request, find_user_data_source, OK_REQUEST_SCHEMA, error_into_message, TOKEN_SECURITY
from web.service.database import get_db_session
from web.view import DataSourceView, DataSourceDatabaseWrite, ProjectView, TableCountsWrite

source = Blueprint('data_source', __name__, url_prefix='/api')


@source.route('/data-source-database', methods=('POST',))
@login_required
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'data_source_database',
            'in': 'body',
            'description': 'Database credentials',
            'required': True,
            'schema': DataSourceDatabaseWrite
        }
    ],
    'responses': {
        200: {
            'description': 'Created new database data source',
            'schema': DataSourceView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_data_source_database():
    validation_errors = DataSourceDatabaseWrite().validate(request.json)
    if validation_errors:
        return bad_request(INVALID_INPUT)

    try:
        proj = find_user_project(request.json['project_id'])
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)

    data_source = DataSource(
        project=proj,
        driver=DataSourceConstants.DRIVER_POSTGRES,
        db=request.json['db'],
        usr=request.json['usr'],
        pwd=request.json['pwd'],
        host=request.json['host'],
        port=request.json['port']
    )
    db_session = get_db_session()
    db_session.add(data_source)
    db_session.commit()
    return DataSourceView().dump(data_source)


@source.route('/data-source-mock-database', methods=('POST',))
@login_required
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'project_id',
            'in': 'formData',
            'description': 'Which project should the mock database belong to',
            'required': True,
            'type': 'integer'
        },
    ],
    'responses': {
        200: {
            'description': 'Created new mock database',
            'schema': DataSourceView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_data_source_mock_database():
    try:
        proj = find_user_project(request.form['project_id'])
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)

    file_name = 'cookies.db'
    factory = FileDataSourceFactory(proj, file_name, current_app.config['PROJECT_STORAGE'])
    try:
        data_source = factory.create_data_source()
        with open(factory.file_path, 'w'):
            pass
    except OSError:
        return bad_request('The file could not be saved')

    engine = DatabaseConnectionManager.create_database_source_engine(data_source)
    mock_meta = create_mock_meta()
    mock_meta.bind = engine
    mock_meta.create_all()

    db_session = get_db_session()
    db_session.add(data_source)
    db_session.commit()
    return DataSourceView().dump(data_source)


@source.route('/data-source-file', methods=('POST',))
@login_required
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'project_id',
            'in': 'formData',
            'description': 'Which project should the resource belong to',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'data_file',
            'in': 'formData',
            'description': 'File with the source data',
            'required': True,
            'type': 'file'
        }
    ],
    'responses': {
        200: {
            'description': 'Created new file data source',
            'schema': DataSourceView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_data_source_file():
    try:
        proj = find_user_project(request.form['project_id'])
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)

    file_param = 'data_file'
    if file_param not in request.files or request.files[file_param].filename == '':
        return bad_request('The file is required')

    file = request.files[file_param]
    file_name = secure_filename(file.filename)
    factory = FileDataSourceFactory(proj, file_name, current_app.config['PROJECT_STORAGE'])
    if not is_file_allowed(file_name):
        return bad_request('This kind of file is not allowed')
    try:
        data_source = factory.create_data_source()
        file.save(factory.file_path)
    except OSError:
        return bad_request('The file could not be saved')

    db_session = get_db_session()
    db_session.add(data_source)
    db_session.commit()
    return DataSourceView().dump(data_source)


def with_data_source_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id: int):
        try:
            data_source = find_user_data_source(id)
        except NoResultFound:
            return bad_request(DATA_SOURCE_NOT_FOUND)
        return view(data_source)
    return wrapped_view


@source.route('/data-source/<id>', methods=('DELETE',))
@login_required
@with_data_source_by_id
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Data source ID to be deleted',
            'required': True,
            'type': 'integer'
        },
    ],
    'responses': {
        200: OK_REQUEST_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def delete_data_source(data_source: DataSource):
    if data_source.file_path is not None:
        try:
            os.remove(data_source.file_path)
        except OSError:
            pass

    # TODO may not be deleted?
    db_session = get_db_session()
    db_session.delete(data_source)
    db_session.commit()
    return ok_request('Deleted the data source')


@source.route('/data-source/<id>/import', methods=('POST',))
@login_required
@with_data_source_by_id
@error_into_message
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Data source ID to import the schema from',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {
            'description': 'Project with the new schema',
            'schema': ProjectView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def import_data_source_schema(data_source: DataSource):
    schema_import = DataSourceSchemaImport(data_source.project)
    db_session = get_db_session()
    schema_import.import_schema(data_source, db_session)
    db_session.commit()
    return ProjectView().dump(data_source.project)


@source.route('/data-source-database/<id>/export', methods=('POST',))
@login_required
@with_data_source_by_id
@error_into_message
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Data source ID to export the data to',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'table_counts',
            'in': 'body',
            'description': 'Which tables and how many rows',
            'required': True,
            'schema': TableCountsWrite
        }
    ],
    'responses': {
        200: OK_REQUEST_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def export_to_data_source(data_source: DataSource):
    if data_source.driver is None:
        return bad_request('The data source is not a database')

    table_counts = request.json['rows_by_table_name']
    database_driver = DatabaseOutputDriver(data_source)
    controller = ProcedureController(data_source.project, table_counts, database_driver)
    # TODO handle errors
    controller.run()
    return ok_request('Successfully filled the database')
