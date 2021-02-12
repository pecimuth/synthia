import functools

from flask import Blueprint, g, request
from sqlalchemy.orm import Session
from flasgger import swag_from
from sqlalchemy.orm.exc import NoResultFound

from core.model.project import Project
from core.service.deserializer import create_mock_meta
from core.service.export import Export
from core.service.output_driver import PreviewOutputDriver
from web.controller.util import find_user_project, bad_request, PROJECT_NOT_FOUND, BAD_REQUEST_SCHEMA
from web.service.extern_db import ExternDb
from core.service.serializer import StructureSerializer
from web.view import ProjectListView, ProjectView, DataSourceListView, PreviewView, TableCountsWrite
from web.controller.auth import login_required
from web.service.database import get_db_session

project = Blueprint('project', __name__, url_prefix='/api')


@project.route('/projects')
@login_required
@swag_from({
    'tags': ['Project'],
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


@project.route('/project/<id>/create-mock-database', methods=('POST',))
@login_required
@with_project_by_id
@swag_from({
    'tags': ['Project'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Project ID',
            'required': True,
            'type': 'integer'
        },
    ],
    'responses': {
        200: {
            'description': 'Created a mock database and returned the project with refreshed schema',
            'schema': ProjectView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_mock_database(proj: Project):
    db_session = get_db_session()

    extern_db = ExternDb(proj)
    meta = create_mock_meta()
    meta.create_all(bind=extern_db.engine)
    delete_schema_from_project(proj, db_session)
    serializer = StructureSerializer(bind=extern_db.engine)
    serializer.add_schema_to_project(proj)
    db_session.commit()

    return ProjectView().dump(proj)


@project.route('/project/<id>/preview', methods=('POST',))
@login_required
@with_project_by_id
@swag_from({
    'tags': ['Project'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Project ID',
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
        200: {
            'description': 'Preview of generated tables',
            'schema': PreviewView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def generate_project_preview(proj: Project):
    # TODO error checking, move to a service
    name_counts = request.json['rows_by_table_name']
    table_counts = []
    for table in proj.tables:
        if table.name in name_counts:
            table_counts.append((table, name_counts[table.name]))
    preview_driver = PreviewOutputDriver(proj, table_counts)
    export = Export(preview_driver)
    # TODO handle errors
    preview = export.generate()
    return PreviewView().dump({'tables': preview})
