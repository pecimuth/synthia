from flasgger import swag_from
from flask import Blueprint, g, request

from web.controller.auth import login_required
from core.model.meta_table import MetaTable
from core.model.project import Project
from web.controller.util import TOKEN_SECURITY, BAD_REQUEST_SCHEMA
from web.service.database import get_db_session
from web.view import TableWrite, TableView

table = Blueprint('table', __name__, url_prefix='/api')


@table.route('/table/<id>', methods=('PATCH',))
@login_required
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
def patch_table(id):
    db_session = get_db_session()

    # TODO not found error
    meta_table = db_session.query(MetaTable).\
        join(MetaTable.project).\
        join(Project.user).\
        filter(
                MetaTable.id == id,
                Project.user == g.user
                ).\
        one()

    validation_errors = TableWrite().validate(request.json)
    if validation_errors:
        return {
            'result': 'error',
            'message': 'Invalid input'
        }

    meta_table.row_count = request.json['row_count']
    db_session.commit()

    return TableView().dump(meta_table)
