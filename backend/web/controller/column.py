from flasgger import swag_from
from flask import Blueprint, g, request

from core.service.column_generator import get_generator_by_name, find_recommended_generator, \
    make_generator_instance_for_meta_column
from web.controller.auth import login_required
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.model.project import Project
from web.controller.util import bad_request, INVALID_INPUT, TOKEN_SECURITY, BAD_REQUEST_SCHEMA
from web.service.database import get_db_session
from web.view import ColumnWrite, ColumnView

column = Blueprint('column', __name__, url_prefix='/api')


@column.route('/column/<id>', methods=('PATCH',))
@login_required
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
def patch_column(id):
    db_session = get_db_session()

    # TODO not found error
    meta_column: MetaColumn = db_session.\
        query(MetaColumn).\
        join(MetaColumn.table).\
        join(MetaTable.project).\
        join(Project.user).\
        filter(
            MetaColumn.id == id,
            Project.user == g.user
        ).\
        one()

    validation_errors = ColumnWrite().validate(request.json)
    if validation_errors:
        return bad_request(INVALID_INPUT)

    generator_instance = make_generator_instance_for_meta_column(meta_column)

    #meta_column.generator_name = request.json['generator_name']
    #meta_column.generator_params = request.json['generator_params']

    if meta_column.data_source is not None:
        generator_instance.estimate_params()

    db_session.commit()
    return ColumnView().dump(meta_column)
