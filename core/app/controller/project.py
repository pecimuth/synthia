import os
from flask import Blueprint, g, request, current_app
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.model.project import Project
from flasgger import swag_from
from app.view import ProjectListView, ProjectView, MessageView
from app.controller.auth import login_required
from app.service.database import get_db_session, get_db_engine
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, create_engine, Integer, String, ForeignKey, DateTime
from app.model.metacolumn import MetaColumn
from app.model.metatable import MetaTable

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
    project = Project(name=request.form['name'], user=g.user)
    db_session = get_db_session()
    db_session.add(project)
    db_session.commit()
    return ProjectView().dump(project)


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


def insert_new_schema(proj: Project, input_engine: Engine, output_session: Session):
    meta = MetaData()
    meta.reflect(bind=input_engine)
    for tab in meta.tables.values():
        meta_table = make_meta_table(tab)
        meta_table.project = proj
        output_session.add(meta_table)


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
def get_project_refresh_schema(id):
    db_session = get_db_session()

    # TODO not found error
    proj = db_session.query(Project).filter(Project.id == id, Project.user == g.user).one()
    delete_schema_from_project(proj, db_session)
    insert_new_schema(proj, get_db_engine(), db_session)
    db_session.commit()

    return ProjectView().dump(proj)


def create_mock_meta() -> MetaData:
    meta = MetaData()
    Table('cookie', meta,
          Column('id', Integer, primary_key=True),
          Column('name', String, nullable=False),
          Column('price', Integer)
          )
    Table('order', meta,
          Column('id', Integer, primary_key=True),
          Column('place', String),
          Column('created_at', DateTime)
          )
    Table('order_item', meta,
          Column('id', Integer, primary_key=True),
          Column('order_id', Integer, ForeignKey('order.id'), nullable=False),
          Column('cookie_id', Integer, ForeignKey('cookie.id'), nullable=False),
          Column('quantity', Integer, nullable=False)
          )
    return meta


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

    db_path = os.path.join(current_app.instance_path, 'project_{}.db'.format(proj.id))
    engine = create_engine('sqlite:///' + db_path)
    meta = create_mock_meta()
    meta.create_all(bind=engine)
    delete_schema_from_project(proj, db_session)
    insert_new_schema(proj, engine, db_session)
    db_session.commit()

    return ProjectView().dump(proj)
