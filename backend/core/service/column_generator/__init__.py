from datetime import datetime
from typing import List, Generic, NamedTuple, TypeVar

ValueType = TypeVar('ValueType', int, float, str, bool, datetime, type(None))


class ColumnGeneratorParam(NamedTuple, Generic[ValueType]):
    name: str
    value_type: str
    default_value: ValueType


ColumnGeneratorParamList = List[ColumnGeneratorParam]
