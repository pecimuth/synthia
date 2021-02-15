from typing import List, Generic, TypeVar, Union, NamedTuple, Literal


ValueType = TypeVar('ValueType', int, str, bool)


class ColumnGeneratorParam(NamedTuple, Generic[ValueType]):
    name: str
    value_type: Literal['number', 'string', 'bool']
    default_value: Union[ValueType, None]


ColumnGeneratorParamList = List[ColumnGeneratorParam]
