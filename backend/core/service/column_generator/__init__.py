import datetime as dt
from typing import List, Generic, NamedTuple, TypeVar

ValueType = TypeVar('ValueType', int, float, str, bool, dt.datetime, type(None))


class ColumnGeneratorParam(NamedTuple, Generic[ValueType]):
    name: str
    value_type: str
    default_value: ValueType


ColumnGeneratorParamList = List[ColumnGeneratorParam]
