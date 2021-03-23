import functools
import json

from flask import Blueprint, g, request, Response
from flasgger import swag_from
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from core.facade.project import ProjectFacade
from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.types import json_serialize_default
from web.controller.util import bad_request, PROJECT_NOT_FOUND, BAD_REQUEST_SCHEMA, TOKEN_SECURITY, \
    FILE_SCHEMA, file_attachment_headers, validate_json, error_into_message
from web.service.injector import inject
from web.view.project import ProjectListView, ProjectView, PreviewView, ExportRequisitionView, \
    ExportFileRequisitionView, SaveView
from web.controller.auth import login_required
from web.service.database import get_db_session

project = Blueprint('project', __name__, url_prefix='/api')


@project.route('/projects')
@login_required
@swag_from({
    'tags': ['Project'],
    'security': TOKEN_SECURITY,
    'responses': {
        200: {
            'description': 'Return users projects',
            'schema': ProjectListView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def get_projects():
    return ProjectListView().dump({'items': g.user.projects})


@project.route('/project', methods=('POST',))
@login_required
@swag_from({
    'tags': ['Project'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'name',
            'in': 'formData',
            'description': 'New project name',
            'required': True,
            'type': 'string'
        },
    ],
    'responses': {
        200: {
            'description': 'Created new project',
            'schema': ProjectView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_project():
    facade = inject(ProjectFacade)
    proj = facade.create_project(request.form['name'])
    get_db_session().commit()
    return ProjectView().dump(proj)


def with_project_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id):
        facade = inject(ProjectFacade)
        try:
            proj = facade.find_project(id)
        except NoResultFound:
            return bad_request(PROJECT_NOT_FOUND)
        return view(proj)
    return wrapped_view


@project.route('/project/<id>')
@login_required
@with_project_by_id
@swag_from({
    'tags': ['Project'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Requested project ID',
            'required': True,
            'type': 'integer'
        },
    ],
    'responses': {
        200: {
            'description': 'Returned project',
            'schema': ProjectView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def get_project(proj: Project):
    return ProjectView().dump(proj)


@project.route('/project/<id>/preview', methods=('POST',))
@login_required
@with_project_by_id
@validate_json(ExportRequisitionView)
@error_into_message
@swag_from({
    'tags': ['Project'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Project ID',
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
        200: {
            'description': 'Preview of generated tables',
            'schema': PreviewView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def generate_project_preview(proj: Project):
    requisition = ExportRequisitionView().load(request.json)
    facade = inject(ProjectFacade)
    tables = facade.generate_preview(proj, requisition)
    get_db_session().commit()
    return PreviewView().dump({'tables': tables})


@project.route('/project/<id>/export', methods=('POST',))
@login_required
@with_project_by_id
@validate_json(ExportFileRequisitionView)
@error_into_message
@swag_from({
    'tags': ['Project'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Project ID',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'requisition',
            'in': 'body',
            'description': 'Export requisition',
            'required': True,
            'schema': ExportFileRequisitionView
        }
    ],
    'responses': {
        200: FILE_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def export_project(proj: Project):
    requisition, driver_name = ExportFileRequisitionView().load(request.json)
    facade = inject(ProjectFacade)
    file_driver = facade.generate_file_export(proj, requisition, driver_name)
    file_name = file_driver.add_extension(secure_filename(proj.name))
    return Response(
        file_driver.dump(),
        mimetype=file_driver.mime_type,
        headers=file_attachment_headers(file_name)
    )


@project.route('/project/<id>/save', methods=('POST',))
@login_required
@with_project_by_id
@validate_json(ExportRequisitionView)
@error_into_message
@swag_from({
    'tags': ['Project'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Project ID',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'requisition',
            'in': 'body',
            'description': 'Export requisition',
            'required': True,
            'schema': ExportRequisitionView
        }
    ],
    'responses': {
        200: {
            'description': 'Project file',
            'schema': {
                'type': 'file'
            }
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def save_project(proj: Project):
    file_name = '{}_proj.json'.format(secure_filename(proj.name))
    py_dump = SaveView().dump({
        'project': proj,
        'requisition': request.json
    })
    json_dump = json.dumps(py_dump, indent=2, default=json_serialize_default)
    return Response(
        json_dump,
        mimetype=DataSourceConstants.MIME_TYPE_JSON,
        headers=file_attachment_headers(file_name)
    )
