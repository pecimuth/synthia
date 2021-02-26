from __future__ import annotations

import random
from abc import ABC
from enum import Enum
from typing import Union, List, Dict, Generic, TypeVar

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.column_generator.params import normalized_params, ParamDict, ColumnGeneratorParamList
from core.service.data_source.data_provider import DataProviderFactory
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')
OutputDict = Dict[str, Union[OutputType, None]]


class GeneratorCategory(Enum):
    GENERAL = 'General'
    ADDRESS = 'Address'
    PERSON = 'Person'
    DATETIME = 'Date & Time'
    TEXT = 'Text'


class RegisteredGenerator(ABC):
    pass


class ColumnGenerator(Generic[OutputType], ABC):
    name: str
    category: GeneratorCategory = GeneratorCategory.GENERAL
    is_database_generated = False
    only_for_type: Union[str, None] = None
    supports_null = True
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

    @property
    def _null_frequency(self) -> float:
        return self._generator_setting.null_frequency

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def make_scalar_or_null(self, generated_database: GeneratedDatabase) -> Union[OutputType, None]:
        if self.supports_null and random.random() < self._null_frequency:
            return None
        return self.make_scalar(generated_database)

    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        raise NotImplemented()

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        return {
            meta_column.name: self.make_scalar_or_null(generated_database)
            for meta_column in self._meta_columns
        }

    def estimate_params(self):
        factory = DataProviderFactory(self._meta_columns)
        provider = factory.find_provider()
        if self.supports_null:
            estimate = provider.estimate_null_frequency()
            if estimate is not None:
                self._generator_setting.null_frequency = estimate
        self._estimate_params_with_provider(provider)

    def _estimate_params_with_provider(self, provider: DataProvider):
        pass
