from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict

from core.model.meta_column import MetaColumn
from core.service.column_generator import ColumnGeneratorParamList
from core.service.data_source.data_provider import create_data_provider
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.exception import SomeError
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import AnyBasicType, convert_value_to_type

OutputType = TypeVar('OutputType')


class ColumnGeneratorBase(Generic[OutputType], ABC):
    name: str
    is_database_generated = False
    param_list: ColumnGeneratorParamList = []

    ParamValue = AnyBasicType
    ParamDict = Dict[str, ParamValue]

    def __init__(self, meta_column: MetaColumn):
        self._meta_column: MetaColumn = meta_column
        self._meta_column.generator_params = self._normalized_params()

    def _normalized_params(self) -> ParamDict:
        result = {}
        for param in self.param_list:
            if self._params and param.name in self._params:
                value = self._meta_column.generator_params[param.name]
                try:
                    result[param.name] = convert_value_to_type(value, param.value_type)
                except (SomeError, ValueError):
                    result[param.name] = param.default_value
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
            raise SomeError('cannot estimate parameters without a data source')
        provider = create_data_provider(self._meta_column)
        self._estimate_params_with_provider(provider)

    def _estimate_params_with_provider(self, provider: DataProvider):
        pass
