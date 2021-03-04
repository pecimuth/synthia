import functools
import json

from flask import Blueprint, g, request, Response
from sqlalchemy.orm import Session
from flasgger import swag_from
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename

from core.model.project import Project
from core.service.data_source import DataSourceConstants
from core.service.generation_procedure.controller import ProcedureController
from core.service.output_driver import PreviewOutputDriver
from core.service.output_driver.file_driver.facade import FileOutputDriverFacade
from core.service.types import json_serialize_default
from web.controller.util import find_user_project, bad_request, PROJECT_NOT_FOUND, BAD_REQUEST_SCHEMA, TOKEN_SECURITY, \
    FILE_SCHEMA, file_attachment_headers, validate_json, error_into_message
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
    proj = Project(name=request.form['name'], user=g.user)
    db_session = get_db_session()
    db_session.add(proj)
    db_session.commit()
    return ProjectView().dump(proj)


def with_project_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id):
        try:
            proj = find_user_project(id)
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


def delete_schema_from_project(proj: Project, session: Session):
    for table in proj.tables:
        for col in table.columns:
            session.delete(col)
        session.delete(table)


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
    preview_driver = PreviewOutputDriver()
    controller = ProcedureController(proj, requisition, preview_driver)
    preview = controller.run()
    return PreviewView().dump({'tables': preview.get_dict()})


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
            'object': ExportFileRequisitionView
        }
    ],
    'responses': {
        200: FILE_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def export_project(proj: Project):
    requisition, driver_name = ExportFileRequisitionView().load(request.json)
    file_driver = FileOutputDriverFacade.make_driver(driver_name)
    controller = ProcedureController(proj, requisition, file_driver)
    controller.run()
    file_name = file_driver.add_extension(secure_filename(proj.name))

    return Response(
        file_driver.dumps(),
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
            'object': ExportRequisitionView
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
