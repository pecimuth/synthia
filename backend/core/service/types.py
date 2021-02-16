from datetime import datetime
from typing import Type, Union

from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.sql.type_api import TypeEngine

from core.service.exception import SomeError

AnyBasicType = Union[int, float, str, bool, datetime, type(None)]


class Types:
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOL = 'bool'
    STRING = 'string'
    DATETIME = 'datetime'
    NONE = 'none'


def get_column_type(column: Column) -> str:
    if isinstance(column.type, Integer):
        return Types.INTEGER
    elif isinstance(column.type, Numeric):
        return Types.FLOAT
    elif isinstance(column.type, Boolean):
        return Types.BOOL
    elif isinstance(column.type, String):
        return Types.STRING
    elif isinstance(column.type, DateTime):
        return Types.DATETIME
    raise SomeError('unknown type {}'.format(column.type.__visit_name__))


def get_sql_alchemy_type(type_literal: str) -> Type[TypeEngine]:
    if type_literal == Types.INTEGER:
        return Integer
    elif type_literal == Types.FLOAT:
        return Numeric
    elif type_literal == Types.BOOL:
        return Boolean
    elif type_literal == Types.STRING:
        return String
    elif type_literal == Types.DATETIME:
        return DateTime
    raise SomeError('unknown type {}'.format(type_literal))


def get_python_type(type_literal: str) -> Type[AnyBasicType]:
    # alchemy_type = get_sql_alchemy_type(type_literal)
    # alchemy_type.python_type
    if type_literal == Types.INTEGER:
        return int
    elif type_literal == Types.FLOAT:
        return float
    elif type_literal == Types.BOOL:
        return bool
    elif type_literal == Types.STRING:
        return str
    elif type_literal == Types.DATETIME:
        return datetime
    raise SomeError('unknown type {}'.format(type_literal))


def convert_value_to_type(value: AnyBasicType, type_literal: str) -> AnyBasicType:
    return get_python_type(type_literal)(value)


def get_value_type(value: AnyBasicType) -> str:
    if isinstance(value, int):
        return Types.INTEGER
    elif isinstance(value, str):
        return Types.STRING
    elif isinstance(value, float):
        return Types.FLOAT
    elif isinstance(value, type(None)):
        return Types.NONE
    elif isinstance(value, datetime):
        return Types.DATETIME
    raise SomeError('unknown value type {}'.format(value))
