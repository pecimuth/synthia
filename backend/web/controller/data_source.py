import functools

from flasgger import swag_from
from flask import Blueprint, request, current_app, Response
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from core.facade.data_source import DataSourceFacade
from core.facade.project import ProjectFacade
from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.data_source.database_common import DatabaseConnectionManager
from core.service.data_source.file_common import FileDataSourceFactory, is_file_allowed
from core.service.deserializer import create_mock_meta
from web.controller.auth import login_required
from web.controller.util import BAD_REQUEST_SCHEMA, bad_request, PROJECT_NOT_FOUND, \
    DATA_SOURCE_NOT_FOUND, ok_request, find_user_data_source, OK_REQUEST_SCHEMA, error_into_message, TOKEN_SECURITY, \
    FILE_SCHEMA, file_attachment_headers, validate_json
from web.service.database import get_db_session
from web.service.injector import inject
from web.view.data_source import DataSourceView, DataSourceDatabaseWrite
from web.view.project import ProjectView, ExportRequisitionView

source = Blueprint('data_source', __name__, url_prefix='/api')


def with_project_from_json(view):
    @functools.wraps(view)
    def wrapped_view():
        facade = inject(ProjectFacade)
        project_id = request.json['project_id']
        try:
            proj = facade.find_project(project_id)
        except NoResultFound:
            return bad_request(PROJECT_NOT_FOUND)
        return view(proj)
    return wrapped_view


@source.route('/data-source-database', methods=('POST',))
@login_required
@validate_json(DataSourceDatabaseWrite)
@with_project_from_json
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
def create_data_source_database(proj: Project):
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
    facade = inject(ProjectFacade)
    project_id = request.form['project_id']
    try:
        proj = facade.find_project(project_id)
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
@with_project_from_json
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
def create_data_source_file(proj: Project):
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


@source.route('/data-source-file/<id>/download')
@login_required
@with_data_source_by_id
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Data source ID to be downloaded',
            'required': True,
            'type': 'integer'
        },
    ],
    'responses': {
        200: FILE_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def download_data_source_file(data_source: DataSource):
    return Response(
        DataSourceFacade.read_file_content(data_source),
        mimetype=data_source.mime_type,
        headers=file_attachment_headers(data_source.file_name)
    )


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
    facade = inject(DataSourceFacade)
    facade.delete(data_source)
    get_db_session().commit()
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
    facade = inject(DataSourceFacade)
    facade.import_schema(data_source)
    get_db_session().commit()
    return ProjectView().dump(data_source.project)


@source.route('/data-source-database/<id>/export', methods=('POST',))
@login_required
@with_data_source_by_id
@error_into_message
@validate_json(ExportRequisitionView)
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
            'name': 'requisition',
            'in': 'body',
            'description': 'Which tables, how many rows and seeds',
            'required': True,
            'schema': ExportRequisitionView
        }
    ],
    'responses': {
        200: OK_REQUEST_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def export_to_data_source(data_source: DataSource):
    requisition = ExportRequisitionView().load(request.json)
    DataSourceFacade.export_to_data_source(data_source, requisition)
    return ok_request('Successfully filled the database')
