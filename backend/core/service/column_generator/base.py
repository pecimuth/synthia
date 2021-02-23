from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union, List, Dict, Generic, TypeVar

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.column_generator.params import normalized_params, ParamDict, ColumnGeneratorParamList
from core.service.data_source.data_provider import DataProviderFactory
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')
OutputDict = Dict[str, OutputType]


class ColumnGeneratorBase(Generic[OutputType], ABC):
    name: str
    is_database_generated = False
    only_for_type: Union[str, None] = None
    param_list: ColumnGeneratorParamList = []

    def __init__(self, generator_setting: GeneratorSetting):
        assert generator_setting.name == self.name
        self._generator_setting = generator_setting
        self._generator_setting.params = \
            normalized_params(self.param_list, self._generator_setting.params)

    @classmethod
    def create_setting_instance(cls) -> GeneratorSetting:
        return GeneratorSetting(name=cls.name)

    @property
    def _meta_column(self) -> MetaColumn:
        return self._generator_setting.columns[0]

    @property
    def _params(self) -> ParamDict:
        return self._generator_setting.params

    @property
    def _meta_columns(self) -> List[MetaColumn]:
        return self._generator_setting.columns

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        raise NotImplemented()

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        return {
            meta_column.name: self.make_scalar(generated_database)
            for meta_column in self._meta_columns
        }

    def estimate_params(self):
        factory = DataProviderFactory(self._meta_columns)
        provider = factory.find_provider()
        self._estimate_params_with_provider(provider)

    def _estimate_params_with_provider(self, provider: DataProvider):
        pass
