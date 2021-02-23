import functools

from flasgger import swag_from
from flask import Blueprint, g, request
from sqlalchemy.orm.exc import NoResultFound

from core.model.generator_setting import GeneratorSetting
from core.service.column_generator import make_generator_instance_for_meta_column
from web.controller.auth import login_required
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.model.project import Project
from web.controller.util import bad_request, INVALID_INPUT, TOKEN_SECURITY, BAD_REQUEST_SCHEMA, COLUMN_NOT_FOUND, \
    find_user_meta_table, TABLE_NOT_FOUND, OK_REQUEST_SCHEMA, ok_request, validate_json
from web.service.database import get_db_session
from web.view import ColumnWrite, ColumnView, ColumnCreate

column = Blueprint('column', __name__, url_prefix='/api')


def validate_setting_id(meta_table: MetaTable, generator_setting_id: int) -> bool:
    # make sure that the generator setting points to the correct table
    # could be handled by the database too
    db_session = get_db_session()
    try:
        db_session.query(GeneratorSetting).\
            filter(
                GeneratorSetting.id == generator_setting_id,
                GeneratorSetting.table == meta_table
            ).one()
    except NoResultFound:
        return False
    return True


def try_patch_column(meta_column: MetaColumn, request_json) -> bool:
    generator_setting_id = request_json.get('generator_setting_id')
    if generator_setting_id is not None and \
       not validate_setting_id(meta_column.table, generator_setting_id):
        return False

    meta_column.generator_setting_id = generator_setting_id
    meta_column.name = request_json['name']
    meta_column.col_type = request_json['col_type']
    meta_column.nullable = request_json['nullable']

    generator_instance = make_generator_instance_for_meta_column(meta_column)
    if meta_column.data_source is not None:
        generator_instance.estimate_params()
    return True


@column.route('/column', methods=('POST',))
@login_required
@validate_json(ColumnCreate)
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
    try:
        meta_table = find_user_meta_table(request.json['table_id'])
    except NoResultFound:
        return bad_request(TABLE_NOT_FOUND)

    meta_column = MetaColumn(table=meta_table)
    if not try_patch_column(meta_column, request.json):
        return bad_request(INVALID_INPUT)

    db_session = get_db_session()
    db_session.commit()
    return ColumnView().dump(meta_column)


def with_column_by_id(view):
    @functools.wraps(view)
    def wrapped_view(id: int):
        try:
            meta_column: MetaColumn = get_db_session().\
                query(MetaColumn).\
                join(MetaColumn.table).\
                join(MetaTable.project).\
                join(Project.user).\
                filter(
                    MetaColumn.id == id,
                    Project.user == g.user
                ).\
                one()
        except NoResultFound:
            return bad_request(COLUMN_NOT_FOUND)
        return view(meta_column)
    return wrapped_view


@column.route('/column/<id>', methods=('PATCH',))
@login_required
@with_column_by_id
@validate_json(ColumnWrite)
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
    if not try_patch_column(meta_column, request.json):
        return bad_request(INVALID_INPUT)
    db_session = get_db_session()
    db_session.commit()
    return ColumnView().dump(meta_column)


@column.route('/column/<id>', methods=('DELETE',))
@login_required
@with_column_by_id
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
        200: OK_REQUEST_SCHEMA,
        400: BAD_REQUEST_SCHEMA
    }
})
def delete_column(meta_column: MetaColumn):
    db_session = get_db_session()
    db_session.delete(meta_column)
    db_session.commit()
    return ok_request('Column deleted')
