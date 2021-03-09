import functools
from typing import Type, Any, List, Dict

from flask import g, request
from marshmallow import Schema
from sqlalchemy.exc import SQLAlchemyError

from core.model.data_source import DataSource
from core.model.project import Project
from core.service.exception import SomeError
from web.service.database import get_db_session
from web.view import MessageView


def ok_request(message: str):
    return {
       'result': 'ok',
       'message': message
    }, 200


def bad_request(message: str, code: int = 400):
    return {
       'result': 'error',
       'message': message
    }, code


OK_REQUEST_SCHEMA = {
    'description': 'Success',
    'schema': MessageView
}

BAD_REQUEST_SCHEMA = {
    'description': 'Bad request',
    'schema': MessageView
}

FILE_SCHEMA = {
    'description': 'File of the requested format',
    'schema': {
        'type': 'file'
    }
}

TOKEN_SECURITY = [
    {
        'APIKeyHeader': [
            'Authorization'
        ]
    }
]


def file_attachment_headers(file_name: str):
    return {
        'Access-Control-Expose-Headers': 'Content-Disposition',
        'Content-Disposition': 'attachment; filename={}'.format(file_name)
    }


def error_into_message(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except SomeError as e:
            return bad_request(e.message)
    return wrapped_view


def patch_from_json(entity: Any, attr: str) -> bool:
    if attr in request.json:
        setattr(entity, attr, request.json[attr])
        return True
    return False


def patch_all_from_json(entity: Any, attrs: List[str]):
    for attr in attrs:
        patch_from_json(entity, attr)


# common error messages
INVALID_INPUT = 'Invalid input'
PROJECT_NOT_FOUND = 'Project not found'
DATA_SOURCE_NOT_FOUND = 'Data source not found'
GENERATOR_SETTING_NOT_FOUND = 'Generator setting not found'
COLUMN_NOT_FOUND = 'Column not found'
TABLE_NOT_FOUND = 'Table not found'


def format_validation_errors(validation_errors: Dict[str, List[str]]) -> str:
    return ', '.join(
        '{}: {}'.format(key, value[0])
        for key, value in validation_errors.items()
    )


def validate_json(schema_factory: Type[Schema]):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            validation_errors = schema_factory().validate(request.json)
            if validation_errors:
                return bad_request(format_validation_errors(validation_errors))
            return view(*args, **kwargs)
        return wrapped_view
    return decorator


def find_user_data_source(data_source_id: int) -> DataSource:
    db_session = get_db_session()
    return db_session.query(DataSource).\
        join(DataSource.project).\
        filter(
            DataSource.id == data_source_id,
            Project.user_id == g.user.id
        ).\
        one()
