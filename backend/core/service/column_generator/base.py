from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, List, Dict, Generic, TypeVar, Optional, Callable, Any

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.column_generator.params import normalized_params, ParamDict, ColumnGeneratorParamList
from core.service.data_source.data_provider import DataProviderFactory
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.exception import GeneratorSettingError
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')
OutputDict = Dict[str, Optional[OutputType]]


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
    is_multi_column: bool
    is_database_generated = False
    only_for_type: Optional[str] = None
    supports_null: bool

    # for decorator implementation
    param_list: ColumnGeneratorParamList = []
    estimator_list: List[Callable[[ColumnGenerator, DataProvider], Any]] = []

    def __init__(self, generator_setting: GeneratorSetting):
        assert generator_setting.name == self.name
        self._generator_setting = generator_setting
        self._generator_setting.params = \
            normalized_params(self, self.param_list, self._generator_setting.params)

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        pass

    @abstractmethod
    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        pass

    @classmethod
    def create_setting_instance(cls) -> GeneratorSetting:
        return GeneratorSetting(name=cls.name)

    @property
    def params(self) -> ParamDict:
        return self._generator_setting.params

    @property
    def _meta_columns(self) -> List[MetaColumn]:
        return self._generator_setting.columns

    def estimate_params(self):
        factory = DataProviderFactory(self._meta_columns)
        provider = factory.find_provider()
        if self.supports_null:
            estimate = provider.estimate_null_frequency()
            if estimate is not None:
                self._generator_setting.null_frequency = estimate
        for estimator in self.estimator_list:
            estimator(self, provider)
        self._estimate_params_with_provider(provider)

    def _estimate_params_with_provider(self, provider: DataProvider):
        pass


class SingleColumnGenerator(Generic[OutputType], ColumnGenerator[OutputType]):
    is_multi_column = False
    supports_null = True

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        if len(generator_setting.columns) != 1:
            raise GeneratorSettingError(
                'wrong number of columns for a single column generator',
                generator_setting
            )

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    @property
    def _null_frequency(self) -> float:
        return self._generator_setting.null_frequency

    @property
    def _meta_column(self) -> MetaColumn:
        return self._generator_setting.columns[0]

    @abstractmethod
    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        pass

    def make_scalar_or_null(self, generated_database: GeneratedDatabase) -> Optional[OutputType]:
        if self.supports_null and random.random() < self._null_frequency:
            return None
        return self.make_scalar(generated_database)

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        return {
            meta_column.name: self.make_scalar_or_null(generated_database)
            for meta_column in self._meta_columns
        }


class MultiColumnGenerator(Generic[OutputType], ColumnGenerator[OutputType]):
    is_multi_column = True
    supports_null = False

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False
