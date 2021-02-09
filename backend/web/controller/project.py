from flask import Blueprint, g, request
from sqlalchemy.orm import Session
from flasgger import swag_from

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.data_source.database import create_database_source_engine
from core.service.deserializer import create_mock_meta
from web.service.extern_db import ExternDb
from web.service.generator.database_generator import DatabaseGenerator
from core.service.serializer import StructureSerializer
from web.view import ProjectListView, ProjectView, MessageView
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
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
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
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def create_project():
    proj = Project(name=request.form['name'], user=g.user)
    db_session = get_db_session()
    db_session.add(proj)
    db_session.commit()
    return ProjectView().dump(proj)


@project.route('/project/<id>')
@login_required
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
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def get_project(id):
    db_session = get_db_session()
    # TODO not found error
    proj = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()
    return ProjectView().dump(proj)


def delete_schema_from_project(proj: Project, session: Session):
    for table in proj.tables:
        for col in table.columns:
            session.delete(col)
        session.delete(table)


@project.route('/project/<id>/refresh-schema', methods=('POST',))
@login_required
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
        {
            'name': 'data_source_id',
            'in': 'formData',
            'description': 'Import from which data source',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {
            'description': 'Returned project with refreshed schema',
            'schema': ProjectView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def refresh_project_schema(id):
    db_session = get_db_session()

    # TODO not found error
    proj = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()
    # TODO do not delete
    delete_schema_from_project(proj, db_session)
    db_session.commit()
    # TODO not found
    data_source = db_session.query(DataSource).\
        filter(
            Project.id == id,
            DataSource.id == request.form['data_source_id']
        ).\
        one()

    engine = create_database_source_engine(data_source)
    serializer = StructureSerializer(bind=engine)
    serializer.add_schema_to_project(proj)
    db_session.commit()

    return ProjectView().dump(proj)


@project.route('/project/<id>/create-mock-database', methods=('POST',))
@login_required
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
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def create_mock_database(id):
    db_session = get_db_session()

    # TODO not found error
    proj = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()

    extern_db = ExternDb(proj)
    meta = create_mock_meta()
    meta.create_all(bind=extern_db.engine)
    delete_schema_from_project(proj, db_session)
    serializer = StructureSerializer(bind=extern_db.engine)
    serializer.add_schema_to_project(proj)
    db_session.commit()

    return ProjectView().dump(proj)


@project.route('/project/<id>/generate', methods=('POST',))
@login_required
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
            'description': 'Filled the database with data',
            'schema': MessageView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def generate(id):
    db_session = get_db_session()

    # TODO not found error
    proj = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()

    gen = DatabaseGenerator(proj)
    gen.fill_database()

    return {
        'result': 'ok',
        'message': 'Successfully filled the database'
    }, 400
