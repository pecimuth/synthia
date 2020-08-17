from flasgger import swag_from
from flask import Blueprint, g, request

from app.controller.auth import login_required
from app.model.meta_table import MetaTable
from app.model.project import Project
from app.service.database import get_db_session
from app.service.generator.table_generator import TableGenerator
from app.view import MessageView, TablePreviewView, TableWrite, TableView

table = Blueprint('table', __name__, url_prefix='/api')


@table.route('/table/<id>/preview')
@login_required
@swag_from({
    'tags': ['Table'],
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
        200: {
            'description': 'Returned table preview',
            'schema': TablePreviewView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def get_preview(id):
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

    gen = TableGenerator(meta_table, {})
    rows = list(gen.make_table_preview(10))

    return TablePreviewView().dump({'rows': rows})


@table.route('/table/<id>', methods=('PATCH',))
@login_required
@swag_from({
    'tags': ['Table'],
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
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
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
