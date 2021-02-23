import functools
from typing import Type

from flask import g, request
from marshmallow import Schema

from core.model.data_source import DataSource
from core.model.meta_table import MetaTable
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

TOKEN_SECURITY = [
    {
        'APIKeyHeader': [
            'Authorization'
        ]
    }
]


def error_into_message(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except SomeError as e:
            return bad_request(e.message)
    return wrapped_view


# common error messages
INVALID_INPUT = 'Invalid input'
PROJECT_NOT_FOUND = 'Project not found'
DATA_SOURCE_NOT_FOUND = 'Data source not found'
GENERATOR_SETTING_NOT_FOUND = 'Generator setting not found'
COLUMN_NOT_FOUND = 'Column not found'
TABLE_NOT_FOUND = 'Table not found'


def validate_json(schema_factory: Type[Schema]):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            validation_errors = schema_factory().validate(request.json)
            if validation_errors:
                return bad_request(INVALID_INPUT)
            return view(*args, **kwargs)
        return wrapped_view
    return decorator


# utility selectors
def find_user_project(project_id: int) -> Project:
    db_session = get_db_session()
    return db_session.query(Project).\
        filter(
            Project.id == project_id,
            Project.user == g.user
        ).\
        one()


def find_user_data_source(data_source_id: int) -> DataSource:
    db_session = get_db_session()
    return db_session.query(DataSource).\
        join(DataSource.project).\
        filter(
            DataSource.id == data_source_id,
            Project.user_id == g.user.id
        ).\
        one()


def find_user_meta_table(meta_table_id: int) -> MetaTable:
    db_session = get_db_session()
    return db_session.query(MetaTable).\
        join(MetaTable.project).\
        filter(
            MetaTable.id == meta_table_id,
            Project.user_id == g.user.id
        ).\
        one()
