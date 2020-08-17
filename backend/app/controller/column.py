from flasgger import swag_from
from flask import Blueprint, g, request

from app.controller.auth import login_required
from app.model.meta_column import MetaColumn
from app.model.meta_table import MetaTable
from app.model.project import Project
from app.service.database import get_db_session
from app.view import MessageView, ColumnWrite, ColumnView

column = Blueprint('column', __name__, url_prefix='/api')


@column.route('/column/<id>', methods=('PATCH',))
@login_required
@swag_from({
    'tags': ['Column'],
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
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def patch_column(id):
    db_session = get_db_session()

    # TODO not found error
    meta_column = db_session.query(MetaColumn).\
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
        return {
            'result': 'error',
            'message': 'Invalid input'
        }

    meta_column.generator_name = request.json['generator_name']
    meta_column.generator_params = request.json['generator_params']
    db_session.commit()

    return ColumnView().dump(meta_column)
