import functools
import os

from flasgger import swag_from
from flask import Blueprint, request, current_app
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from core.model.data_source import DataSource
from core.service.data_source import DataSourceUtil
from core.service.data_source.database import create_database_source_engine
from core.service.serializer import StructureSerializer
from web.controller.auth import login_required
from web.controller.util import BAD_REQUEST_SCHEMA, bad_request, find_user_project, PROJECT_NOT_FOUND, INVALID_INPUT, \
    DATA_SOURCE_NOT_FOUND, ok_request, find_user_data_source, OK_REQUEST_SCHEMA
from web.service.database import get_db_session
from core.service.generator.database_generator import DatabaseGenerator
from web.view import DataSourceView, DataSourceDatabaseWrite, ProjectView

source = Blueprint('data_source', __name__, url_prefix='/api')


@source.route('/data-source-database', methods=('POST',))
@login_required
@swag_from({
    'tags': ['DataSource'],
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
        driver=DataSourceUtil.DRIVER_POSTGRES,
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


@source.route('/data-source-file', methods=('POST',))
@login_required
@swag_from({
    'tags': ['DataSource'],
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
    ds_util = DataSourceUtil(proj, current_app.config['PROJECT_STORAGE'])
    file_name = secure_filename(file.filename)
    if not ds_util.is_file_allowed(file_name):
        return bad_request('This kind of file is not allowed')
    directory = ds_util.get_directory()
    file_path = ds_util.get_file_path(file_name)
    try:
        if os.path.exists(file_path):
            return bad_request('A data source with the same name already exists')
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        return bad_request('The file could not be saved')
    file.save(file_path)
    data_source = ds_util.create_file_data_source(file_name)
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
    if data_source.file_name is not None:
        ds_util = DataSourceUtil(data_source.project, current_app.config['PROJECT_STORAGE'])
        try:
            os.remove(ds_util.get_file_path(data_source.file_name))
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
@swag_from({
    'tags': ['DataSource'],
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
    # TODO choose appropriate schema provider
    engine = create_database_source_engine(data_source)
    serializer = StructureSerializer(bind=engine)
    serializer.add_schema_to_project(data_source.project)
    get_db_session().commit()

    return ProjectView().dump(data_source.project)


@source.route('/data-source-database/<id>/export', methods=('POST',))
@login_required
@with_data_source_by_id
@swag_from({
    'tags': ['DataSource'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Data source ID to export the data to',
            'required': True,
            'type': 'integer'
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

    gen = DatabaseGenerator(data_source)
    # TODO handle errors
    gen.fill_database()

    return ok_request('Successfully filled the database')
