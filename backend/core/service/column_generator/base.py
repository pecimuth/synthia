from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Union

from core.model.meta_column import MetaColumn
from core.service.column_generator import ColumnGeneratorParamList, ColumnGeneratorParam
from core.service.data_source.data_provider import create_data_provider
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')


class ColumnGeneratorBase(Generic[OutputType], ABC):
    name: str
    is_database_generated = False
    param_list: ColumnGeneratorParamList = []

    ParamValue = Union[str, int, bool]
    ParamDict = Dict[str, ParamValue]

    def __init__(self, meta_column: MetaColumn):
        self._meta_column: MetaColumn = meta_column
        self._meta_column.generator_params = self._prepare_params()

    @classmethod
    def _convert_param_value(cls, param: ColumnGeneratorParam, value) -> ParamValue:
        if param.value_type == 'number' and not isinstance(value, int):
            return int(value)
        if param.value_type == 'bool' and not isinstance(value, bool):
            return value == 'true'
        return value

    def _prepare_params(self) -> ParamDict:
        result = {}
        for param in self.param_list:
            if self._meta_column.generator_params and \
               param.name in self._meta_column.generator_params:
                value = self._meta_column.generator_params[param.name]
                converted = self._convert_param_value(param, value)
                result[param.name] = converted
            else:
                result[param.name] = param.default_value
        return result

    @property
    def _params(self) -> dict:
        return self._meta_column.generator_params

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def make_value(self, generated_database: GeneratedDatabase) -> OutputType:
        pass

    def estimate_params(self):
        data_source = self._meta_column.data_source
        if data_source is None:
            raise Exception('cannot estimate parameters without a data source')
        provider = create_data_provider(self._meta_column)
        self._estimate_params_with_provider(provider)

    def _estimate_params_with_provider(self, provider: DataProvider):
        pass
