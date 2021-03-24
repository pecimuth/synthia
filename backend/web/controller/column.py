import functools

from flasgger import swag_from
from flask import Blueprint, request
from sqlalchemy.orm.exc import NoResultFound

from core.facade.column import ColumnFacade
from core.facade.generator import GeneratorFacade
from core.facade.project import ProjectFacade
from core.facade.table import TableFacade
from web.controller.auth import login_required
from core.model.meta_column import MetaColumn
from web.controller.util import bad_request, INVALID_INPUT, TOKEN_SECURITY, BAD_REQUEST_SCHEMA, COLUMN_NOT_FOUND, \
    TABLE_NOT_FOUND, validate_json, patch_all_from_json, \
    error_into_message
from web.service.database import get_db_session
from web.service.injector import inject
from web.view.column import ColumnWrite, ColumnView, ColumnCreate
from web.view.project import ProjectView

column = Blueprint('column', __name__, url_prefix='/api')


def try_patch_column(meta_column: MetaColumn) -> bool:
    """Try to patch the meta column from request.json.
    Return operation status.

    Generator assignment must be checked for errors.
    """
    patch_all_from_json(meta_column, ['name', 'col_type', 'nullable'])

    generator_setting_id = request.json.get('generator_setting_id')
    if generator_setting_id is not None:
        facade = inject(GeneratorFacade)
        return facade.update_column_generator(meta_column, generator_setting_id)
    return True


@column.route('/column', methods=('POST',))
@login_required
@validate_json(ColumnCreate)
@error_into_message
@swag_from({
    'tags': ['Column'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'column',
            'in': 'body',
            'description': 'Column content',
            'required': True,
            'schema': ColumnCreate
        }
    ],
    'responses': {
        200: {
            'description': 'Returned new column',
            'schema': ColumnView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def create_column():
    facade = inject(TableFacade)
    try:
        meta_table = facade.find_meta_table(request.json['table_id'])
    except NoResultFound:
        return bad_request(TABLE_NOT_FOUND)

    meta_column = MetaColumn(table=meta_table)
    if not try_patch_column(meta_column):
        return bad_request(INVALID_INPUT)

    db_session = get_db_session()
    db_session.commit()
    return ColumnView().dump(meta_column)


def with_column_by_id(view):
    """Decorator for handlers accepting column ID in path.

    Fetches the column by ID and calls the handler with the column
    instance instead of the ID.
    """
    @functools.wraps(view)
    def wrapped_view(id: int):
        facade = inject(ColumnFacade)
        try:
            meta_column = facade.find_column(id)
        except NoResultFound:
            return bad_request(COLUMN_NOT_FOUND)
        return view(meta_column)
    return wrapped_view


@column.route('/column/<id>', methods=('PATCH',))
@login_required
@with_column_by_id
@validate_json(ColumnWrite)
@error_into_message
@swag_from({
    'tags': ['Column'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Column ID',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'column',
            'in': 'body',
            'description': 'Column content',
            'required': True,
            'schema': ColumnWrite
        }
    ],
    'responses': {
        200: {
            'description': 'Returned patched column',
            'schema': ColumnView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def patch_column(meta_column: MetaColumn):
    if not try_patch_column(meta_column):
        return bad_request(INVALID_INPUT)
    db_session = get_db_session()
    db_session.commit()
    return ColumnView().dump(meta_column)


@column.route('/column/<id>', methods=('DELETE',))
@login_required
@with_column_by_id
@error_into_message
@swag_from({
    'tags': ['Column'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'Column ID',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {
            'description': 'Updated project schema',
            'schema': ProjectView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def delete_column(meta_column: MetaColumn):
    project_id = meta_column.table.project_id
    facade = inject(ColumnFacade)
    facade.delete(meta_column)
    get_db_session().commit()
    project_facade = inject(ProjectFacade)
    project = project_facade.find_project(project_id)
    return ProjectView().dump(project)
