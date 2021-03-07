from abc import ABC
from datetime import datetime, date
from typing import Type, Union, Optional

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


class TypeDefinition(ABC):
    type_literal: Types
    python_type: Type[AnyBasicType]
    alchemy_type: Optional[Type[TypeEngine]]


class BoolTypeDefinition(TypeDefinition):
    type_literal = Types.BOOL
    python_type = bool
    alchemy_type = Boolean


class IntegerTypeDefinition(TypeDefinition):
    type_literal = Types.INTEGER
    python_type = int
    alchemy_type = Integer


class FloatTypeDefinition(TypeDefinition):
    type_literal = Types.FLOAT
    python_type = float
    alchemy_type = Numeric


class StringTypeDefinition(TypeDefinition):
    type_literal = Types.STRING
    python_type = str
    alchemy_type = String


class DateTimeTypeDefinition(TypeDefinition):
    type_literal = Types.DATETIME
    python_type = datetime
    alchemy_type = DateTime


class NoneTypeDefinition(TypeDefinition):
    type_literal = Types.NONE
    python_type = type(None)
    alchemy_type = None


def get_column_type(column: Column) -> Types:
    for type_def in TypeDefinition.__subclasses__():
        if isinstance(column.type, type_def.alchemy_type):
            return type_def.type_literal
    raise SomeError('Unknown column type {}'.format(column.type.__visit_name__))


def get_sql_alchemy_type(type_literal: Types) -> Type[TypeEngine]:
    for type_def in TypeDefinition.__subclasses__():
        if type_literal == type_def.type_literal:
            return type_def.alchemy_type
    raise SomeError('Unknown type literal {}'.format(type_literal))


def get_python_type(type_literal: Types) -> Type[AnyBasicType]:
    for type_def in TypeDefinition.__subclasses__():
        if type_literal == type_def.type_literal:
            return type_def.python_type
    raise SomeError('Unknown type literal {}'.format(type_literal))


def convert_value_to_type(value: AnyBasicType, type_literal: Types) -> AnyBasicType:
    if type_literal == Types.DATETIME and isinstance(value, str):
        return datetime.strptime(value, DATETIME_FORMAT)
    return get_python_type(type_literal)(value)


def get_value_type(value: AnyBasicType) -> Types:
    for type_def in TypeDefinition.__subclasses__():
        if isinstance(value, type_def.python_type):
            return type_def.type_literal
    raise SomeError('Unknown value type {}'.format(value))


def class_to_types(cls) -> Types:
    for type_def in TypeDefinition.__subclasses__():
        if cls == type_def.python_type:
            return type_def.type_literal
    raise SomeError('Unknown class {}'.format(cls))
