import functools

from flasgger import swag_from
from flask import Blueprint, g, request
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from core.model.generator_setting import GeneratorSetting
from core.model.meta_constraint import MetaConstraint
from core.service.column_generator.assignment import GeneratorAssignment
from core.service.column_generator.setting_facade import GeneratorSettingFacade
from web.controller.auth import login_required
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.model.project import Project
from web.controller.util import bad_request, INVALID_INPUT, TOKEN_SECURITY, BAD_REQUEST_SCHEMA, COLUMN_NOT_FOUND, \
    find_user_meta_table, TABLE_NOT_FOUND, OK_REQUEST_SCHEMA, ok_request, validate_json, patch_all_from_json, \
    patch_from_json, error_into_message
from web.service.database import get_db_session
from web.view.column import ColumnWrite, ColumnView, ColumnCreate

column = Blueprint('column', __name__, url_prefix='/api')


def get_generator_setting(generator_setting_id: int, meta_table: MetaTable) -> GeneratorSetting:
    # make sure that the generator setting points to the correct table
    db_session = get_db_session()
    return db_session.query(GeneratorSetting).\
        filter(
            GeneratorSetting.id == generator_setting_id,
            GeneratorSetting.table == meta_table
        ).one()


def try_patch_column(meta_column: MetaColumn) -> bool:
    patch_all_from_json(meta_column, ['name', 'col_type', 'nullable'])

    if 'generator_setting_id' in request.json:
        generator_setting_id = request.json['generator_setting_id']
        generator_setting = get_generator_setting(generator_setting_id, meta_column.table)

        if not GeneratorAssignment.maybe_assign(generator_setting, meta_column):
            return False

        facade = GeneratorSettingFacade(generator_setting)
        facade.maybe_estimate_params()
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
    try:
        meta_table = find_user_meta_table(request.json['table_id'])
    except NoResultFound:
        return bad_request(TABLE_NOT_FOUND)

    meta_column = MetaColumn(table=meta_table)
    if not try_patch_column(meta_column):
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

    column_constraints =\
        db_session.query(MetaConstraint.id).\
        join(MetaConstraint.constrained_columns).\
        filter(MetaColumn.id == meta_column.id)

    referencing_constraints =\
        db_session.query(MetaConstraint.id).\
        join(MetaConstraint.referenced_columns).\
        filter(MetaColumn.id == meta_column.id)

    db_session.query(MetaConstraint).\
        filter(
            or_(
                MetaConstraint.id.in_(referencing_constraints.subquery()),
                MetaConstraint.id.in_(column_constraints.subquery())
            )
        ).\
        delete(synchronize_session=False)

    db_session.delete(meta_column)
    db_session.commit()
    return ok_request('Column deleted')
