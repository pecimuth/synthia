import functools

from flasgger import swag_from
from flask import Blueprint, request
from sqlalchemy.orm.exc import NoResultFound

from core.facade.project import ProjectFacade
from core.facade.table import TableFacade
from core.model.meta_table import MetaTable
from web.controller.auth import login_required
from web.controller.util import TOKEN_SECURITY, BAD_REQUEST_SCHEMA, TABLE_NOT_FOUND, \
    bad_request, OK_REQUEST_SCHEMA, ok_request, PROJECT_NOT_FOUND, validate_json
from web.service.database import get_db_session
from web.service.injector import inject
from web.view.table import TableWrite, TableView, TableCreate

table = Blueprint('table', __name__, url_prefix='/api')


def with_table_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id: int):
        facade = inject(TableFacade)
        try:
            meta_table = facade.find_meta_table(id)
        except NoResultFound:
            return bad_request(TABLE_NOT_FOUND)
        return view(meta_table)
    return wrapped_view


def try_patch_table(meta_table: MetaTable, request_json):
    meta_table.name = request_json['name']


@table.route('/table', methods=('POST',))
@login_required
@validate_json(TableCreate)
@swag_from({
    'tags': ['Table'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'table',
            'in': 'body',
            'description': 'Table content',
            'required': True,
            'schema': TableCreate
        }
    ],
    'responses': {
        200: {
            'description': 'Created table',
            'schema': TableView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_table():
    facade = inject(ProjectFacade)
    project_id = request.json['project_id']
    try:
        project = facade.find_project(project_id)
    except NoResultFound:
        return bad_request(PROJECT_NOT_FOUND)

    meta_table = MetaTable(project=project)
    try_patch_table(meta_table, request.json)
    db_session = get_db_session()
    db_session.commit()
    return TableView().dump(meta_table)


@table.route('/table/<id>', methods=('PATCH',))
@login_required
@with_table_by_id
@validate_json(TableWrite)
@swag_from({
    'tags': ['Table'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Table ID',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'table',
            'in': 'body',
            'description': 'Table content',
            'required': True,
            'schema': TableWrite
        }
    ],
    'responses': {
        200: {
            'description': 'Returned patched table',
            'schema': TableView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def patch_table(meta_table: MetaTable):
    try_patch_table(meta_table, request.json)
    db_session = get_db_session()
    db_session.commit()
    return TableView().dump(meta_table)


@table.route('/table/<id>', methods=('DELETE',))
@login_required
@with_table_by_id
@swag_from({
    'tags': ['Table'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Table ID',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: OK_REQUEST_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def delete_table(meta_table: MetaTable):
    facade = inject(TableFacade)
    facade.delete(meta_table)
    get_db_session().commit()
    return ok_request('Deleted the table')
