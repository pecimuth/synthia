import functools

from flasgger import swag_from
from flask import Blueprint, request, Response
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from core.facade.data_source import DataSourceFacade
from core.facade.project import ProjectFacade
from core.model.data_source import DataSource
from web.controller.auth import login_required
from web.controller.util import BAD_REQUEST_SCHEMA, bad_request, PROJECT_NOT_FOUND, \
    DATA_SOURCE_NOT_FOUND, ok_request, OK_REQUEST_SCHEMA, error_into_message, TOKEN_SECURITY, \
    FILE_SCHEMA, file_attachment_headers, validate_json, patch_all_from_json
from web.service.database import get_db_session
from web.service.injector import inject
from web.view.data_source import DataSourceView, DataSourceDatabaseWrite, DataSourceDatabaseCreate
from web.view.project import ProjectView, ExportRequisitionView

source = Blueprint('data_source', __name__, url_prefix='/api')


def patch_database_data_source(data_source: DataSource):
    patch_all_from_json(data_source, ['driver', 'db', 'usr', 'pwd', 'host', 'port'])


def with_data_source_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id: int):
        facade = inject(DataSourceFacade)
        try:
            data_source = facade.find_data_source(id)
        except NoResultFound:
            return bad_request(DATA_SOURCE_NOT_FOUND)
        return view(data_source)
    return wrapped_view


@source.route('/data-source-database', methods=('POST',))
@login_required
@validate_json(DataSourceDatabaseCreate)
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'data_source_database',
            'in': 'body',
            'description': 'Database credentials',
            'required': True,
            'schema': DataSourceDatabaseCreate
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
    facade = inject(ProjectFacade)
    project_id = request.json['project_id']
    try:
        proj = facade.find_project(project_id)
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)
    data_source = DataSource(project=proj)
    patch_database_data_source(data_source)
    db_session = get_db_session()
    db_session.add(data_source)
    db_session.commit()
    return DataSourceView().dump(data_source)


@source.route('/data-source-database/<id>', methods=('PATCH',))
@login_required
@validate_json(DataSourceDatabaseWrite)
@with_data_source_by_id
@swag_from({
    'tags': ['DataSource'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Data source ID',
            'required': True,
            'type': 'integer'
        },
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
            'description': 'Patched data source',
            'schema': DataSourceView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def patch_data_source_database(data_source: DataSource):
    patch_database_data_source(data_source)
    get_db_session().commit()
    return DataSourceView().dump(data_source)


@source.route('/data-source-mock-database', methods=('POST',))
@login_required
@error_into_message
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
    project_id = request.form['project_id']
    data_source_facade = inject(DataSourceFacade)
    try:
        data_source = data_source_facade.create_mock_database(project_id)
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)
    get_db_session().commit()
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
    file_param = 'data_file'
    if file_param not in request.files or request.files[file_param].filename == '':
        return bad_request('The file is required')

    project_id = request.form['project_id']
    file = request.files[file_param]
    file_name = secure_filename(file.filename)
    data_source_facade = inject(DataSourceFacade)
    try:
        data_source = data_source_facade.create_data_source_for_file(project_id, file_name)
        file.save(data_source.file_path)
    except OSError:
        return bad_request('The file could not be saved')
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)

    get_db_session().commit()
    return DataSourceView().dump(data_source)


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
    facade = inject(DataSourceFacade)
    facade.export_to_data_source(data_source, requisition)
    return ok_request('Successfully filled the database')
