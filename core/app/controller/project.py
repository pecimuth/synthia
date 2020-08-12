from flask import Blueprint, g, request
from app.model.project import Project
from flasgger import swag_from
from app.view import ProjectListView, ProjectView
from app.controller.auth import login_required
from app.service.database import get_db_session, get_db_engine
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column
from app.model.metacolumn import MetaColumn
from app.model.metatable import MetaTable

project = Blueprint('project', __name__, url_prefix='/api')

@login_required
@project.route('/projects')
@swag_from({
    'tags': ['Project'],
    'responses': {
        200: {
            'description': 'Return users projects',
            'schema': ProjectListView
        },
        400: {
            'description': 'Bad request'
        }
    }
})
def get_projects():
    return ProjectListView().dump({'items': g.user.projects})

@login_required
@project.route('/project', methods=('POST',))
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
        400: {
            'description': 'Bad request'
        }
    }
})
def create_project():
    project = Project(name=request.form['name'], user=g.user)
    db_session = get_db_session()
    db_session.add(project)
    db_session.commit()
    return ProjectView().dump(project)

@login_required
@project.route('/project/<id>')
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
        400: {
            'description': 'Bad request'
        }
    }
})
def get_project(id):
    db_session = get_db_session()
    # TODO not found error
    project = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()
    return ProjectView().dump(project)

def make_meta_column(column: Column) -> MetaColumn:
    return MetaColumn(
        name=column.name,
        primary_key=column.primary_key,
        col_type=column.type.__visit_name__,
        nullable=column.nullable
    )

def make_meta_table(table: Table) -> MetaTable:
    return MetaTable(
        name=table.name,
        columns=[make_meta_column(col) for col in table.c.values()]
    )

@login_required
@project.route('/project/<id>/refresh-schema', methods=('POST',))
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
            'description': 'Returned project with refreshed schema',
            'schema': ProjectView
        },
        400: {
            'description': 'Bad request'
        }
    }
})
def get_project_refresh_schema(id):
    db_session = get_db_session()

    # TODO not found error
    project = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()
    
    meta = MetaData()
    meta.reflect(bind=get_db_engine())
    for tab in meta.tables.values():
        meta_table = make_meta_table(tab)
        meta_table.project = project
        db_session.add(meta_table)
    db_session.commit()

    return ProjectView().dump(project)
