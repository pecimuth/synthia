import datetime as dt
from dataclasses import dataclass
from typing import List, Generic, TypeVar, Union, Dict

from core.service.exception import SomeError
from core.service.types import convert_value_to_type, AnyBasicType

ValueType = TypeVar('ValueType', int, float, str, bool, dt.datetime, type(None))


@dataclass
class ColumnGeneratorParam(Generic[ValueType]):
    name: str
    value_type: str
    default_value: ValueType

    # constraints
    min_value: ValueType = None
    max_value: ValueType = None
    greater_equal_than: Union[str, None] = None


ColumnGeneratorParamList = List[ColumnGeneratorParam]
ParamDict = Dict[str, AnyBasicType]
ParamDictOrNone = Union[ParamDict, None]


def normalized_params(param_list: ColumnGeneratorParamList, param_dict: ParamDictOrNone) -> ParamDict:
    result = {}
    for param in param_list:
        if param_dict and param.name in param_dict:
            value = param_dict[param.name]
            try:
                result[param.name] = convert_value_to_type(value, param.value_type)
            except (SomeError, ValueError):
                result[param.name] = param.default_value
        else:
            result[param.name] = param.default_value
    enforce_param_constraints(param_list, result)
    return result


def enforce_param_constraints(param_list: ColumnGeneratorParamList, param_dict: ParamDict):
    # greater than constraints enforced by swapping the values
    for param in param_list:
        if param.greater_equal_than is not None and \
           param_dict[param.name] < param_dict[param.greater_equal_than]:
            param_dict[param.name], param_dict[param.greater_equal_than] = \
                param_dict[param.greater_equal_than], param_dict[param.name]
    # clamp according to min, max
    for param in param_list:
        if param.min_value is not None and param_dict[param.name] < param.min_value:
            param_dict[param.name] = param.min_value
        elif param.max_value is not None and param_dict[param.name] > param.max_value:
            param_dict[param.name] = param.max_value
