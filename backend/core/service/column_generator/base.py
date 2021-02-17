from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union

from core.model.meta_column import MetaColumn
from core.service.column_generator.params import normalized_params, ParamDict, ColumnGeneratorParamList
from core.service.data_source.data_provider import create_data_provider
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.exception import SomeError
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')


class ColumnGeneratorBase(Generic[OutputType], ABC):
    name: str
    is_database_generated = False
    only_for_type: Union[str, None] = None
    param_list: ColumnGeneratorParamList = []

    def __init__(self, meta_column: MetaColumn):
        self._meta_column: MetaColumn = meta_column
        self._meta_column.generator_params = \
            normalized_params(self.param_list, self._meta_column.generator_params)

    @property
    def _params(self) -> ParamDict:
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
