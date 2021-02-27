from datetime import datetime, date
from typing import Type, Union

from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Enum
from sqlalchemy.sql.type_api import TypeEngine

from core.service.exception import SomeError

AnyBasicType = Union[int, float, str, bool, datetime, type(None)]

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def json_serialize_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime(DATETIME_FORMAT)
    return str(obj)


class Types(Enum):
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


def get_sql_alchemy_type(type_literal: Types) -> Type[TypeEngine]:
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


def get_python_type(type_literal: Types) -> Type[AnyBasicType]:
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


def convert_value_to_type(value: AnyBasicType, type_literal: Types) -> AnyBasicType:
    if type_literal == Types.DATETIME and isinstance(value, str):
        return datetime.strptime(value, DATETIME_FORMAT)
    return get_python_type(type_literal)(value)


def get_value_type(value: AnyBasicType) -> Types:
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


def class_to_types(cls) -> Types:
    if cls == int:
        return Types.INTEGER
    elif cls == str:
        return Types.STRING
    elif cls == float:
        return Types.FLOAT
    elif cls == type(None):
        return Types.NONE
    elif cls == datetime:
        return Types.DATETIME
    raise SomeError('unknown class')
