import functools
from typing import Type, Any, List, Dict

from flask import request
from marshmallow import Schema

from core.service.exception import SomeError
from web.service.database import get_db_session
from web.view import MessageView


def ok_request(message: str):
    """Format ok response from a message."""
    return {
       'result': 'ok',
       'message': message
    }, 200


def bad_request(message: str, code: int = 400):
    """Format bad request response from a message."""
    return {
       'result': 'error',
       'message': message
    }, code


OK_REQUEST_SCHEMA = {
    'description': 'Success',
    'schema': MessageView
}
"""API schema of the response returned by ok_request."""

BAD_REQUEST_SCHEMA = {
    'description': 'Bad request',
    'schema': MessageView
}
"""API schema of the response returned by bad_request."""

FILE_SCHEMA = {
    'description': 'File of the requested format',
    'schema': {
        'type': 'file'
    }
}
"""API schema of a file in a response."""

TOKEN_SECURITY = [
    {
        'APIKeyHeader': [
            'Authorization'
        ]
    }
]
"""API schema of a security header."""


def file_attachment_headers(file_name: str):
    """Return HTTP headers of a file attachment."""
    return {
        'Access-Control-Expose-Headers': 'Content-Disposition',
        'Content-Disposition': 'attachment; filename={}'.format(file_name)
    }


def error_into_message(view):
    """Endpoint handler decorator. Catch all errors in our error hierarchy
    and convert them into bad requests with error messages."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except SomeError as e:
            get_db_session().rollback()
            return bad_request(e.message)
    return wrapped_view


def patch_from_json(entity: Any, attr: str) -> bool:
    """Patch an entity's attribute given by name from request.json.

    Useful in a PATCH request handler. We check that the attribute
    is present in the request.json. If so, the entity's attribute
    of the same is updated.
    """
    if attr in request.json:
        setattr(entity, attr, request.json[attr])
        return True
    return False


def patch_all_from_json(entity: Any, attrs: List[str]):
    """Try to patch all attributes of an entity from request.json
    list by attribute names.
    """
    for attr in attrs:
        patch_from_json(entity, attr)


# common error messages
INVALID_INPUT = 'Invalid input'
PROJECT_NOT_FOUND = 'Project not found'
DATA_SOURCE_NOT_FOUND = 'Data source not found'
GENERATOR_SETTING_NOT_FOUND = 'Generator setting not found'
COLUMN_NOT_FOUND = 'Column not found'
TABLE_NOT_FOUND = 'Table not found'
EMAIL_ALREADY_REGISTERED = 'This email is already registered'


def format_validation_errors(validation_errors: Dict[str, List[str]]) -> str:
    """Return marshmallow validation errors formatted as a single string."""
    return ', '.join(
        '{}: {}'.format(key, value[0])
        for key, value in validation_errors.items()
    )


def validate_json(schema_factory: Type[Schema]):
    """Endpoint handler decorator which handles schema validation.

    If there are any errors, bad request is returned with formatted validation errors..
    """
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            validation_errors = schema_factory().validate(request.json)
            if validation_errors:
                return bad_request(format_validation_errors(validation_errors))
            return view(*args, **kwargs)
        return wrapped_view
    return decorator
