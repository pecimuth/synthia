from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum
from inspect import signature
from typing import List, Dict, Generic, TypeVar, Optional, Callable, Any, Type, Iterable

from sqlalchemy.orm.attributes import flag_modified

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.column_generator.params import normalized_params, ParamDict, ColumnGeneratorParamList
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.exception import GeneratorSettingError, GeneratorRegistrationError, SomeError
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import class_to_types, Types

OutputType = TypeVar('OutputType')
OutputDict = Dict[str, Optional[OutputType]]


class GeneratorCategory(Enum):
    GENERAL = 'General'
    ADDRESS = 'Address'
    PERSON = 'Person'
    DATETIME = 'Date & Time'
    TEXT = 'Text'


class ColumnGenerator(Generic[OutputType], ABC):
    category: GeneratorCategory = GeneratorCategory.GENERAL
    is_database_generated = False
    supports_null: bool

    # for decorator implementation
    param_list: ColumnGeneratorParamList = []
    estimator_list: List[Callable[[ColumnGenerator, DataProvider], Any]] = []

    def __init__(self, generator_setting: GeneratorSetting):
        assert generator_setting.name == self.name()
        self._random = random.Random()
        self._generator_setting = generator_setting
        self._generator_setting.params = \
            normalized_params(self, self.param_list, self._generator_setting.params)
        flag_modified(generator_setting, 'params')  # register the param change

    @classmethod
    def name(cls):
        cls_name: str = cls.__name__
        suffix = 'Generator'
        if cls_name.endswith(suffix):
            return cls_name[:-len(suffix)]
        return cls_name

    @classmethod
    @abstractmethod
    def only_for_type(cls) -> Optional[Types]:
        pass

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        pass

    def seed(self, seed: float):
        self._random.seed(seed)

    @abstractmethod
    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        pass

    @classmethod
    def create_setting_instance(cls) -> GeneratorSetting:
        return GeneratorSetting(name=cls.name())

    @property
    def setting(self) -> GeneratorSetting:
        return self._generator_setting

    @property
    def params(self) -> ParamDict:
        return self._generator_setting.params

    @property
    def _meta_columns(self) -> List[MetaColumn]:
        return self._generator_setting.columns

    def estimate_params(self, provider: DataProvider):
        if self.supports_null:
            estimate = provider.estimate_null_frequency()
            if estimate is not None:
                self._generator_setting.null_frequency = estimate
        for estimator in self.estimator_list:
            estimator(self, provider)


class RegisteredGenerator(ABC):
    _by_name: Optional[Dict[str, Type[ColumnGenerator]]] = None

    @classmethod
    def _make_dict(cls):
        cls._by_name = {}
        for column_gen in RegisteredGenerator.__subclasses__():
            if not issubclass(column_gen, ColumnGenerator):
                raise GeneratorRegistrationError()
            cls._by_name[column_gen.name()] = column_gen

    @classmethod
    def _require_dict(cls):
        if cls._by_name is None:
            cls._make_dict()

    @classmethod
    def is_name_registered(cls, name: str) -> bool:
        cls._require_dict()
        return name in cls._by_name

    @classmethod
    def get_by_name(cls, name: str) -> Type[ColumnGenerator[OutputType]]:
        if not cls.is_name_registered(name):
            raise SomeError('invalid generator name')
        return cls._by_name[name]

    @classmethod
    def iter(cls) -> Iterable[Type[ColumnGenerator]]:
        cls._require_dict()
        return cls._by_name.values()


class SingleColumnGenerator(Generic[OutputType], ColumnGenerator[OutputType]):
    supports_null = True

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        if len(generator_setting.columns) != 1:
            raise GeneratorSettingError(
                'wrong number of columns for a single column generator',
                generator_setting
            )

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        sig = signature(cls.make_scalar)
        klass = sig.return_annotation
        if not isinstance(klass, TypeVar):
            return class_to_types(klass)
        return None

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
        if self.supports_null and self._random.random() < self._null_frequency:
            return None
        return self.make_scalar(generated_database)

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        return {
            meta_column.name: self.make_scalar_or_null(generated_database)
            for meta_column in self._meta_columns
        }


class MultiColumnGenerator(Generic[OutputType], ColumnGenerator[OutputType], ABC):
    supports_null = False

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return None

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def should_unite_with(self, meta_column: MetaColumn) -> bool:
        return self.is_recommended_for(meta_column)

    def unite_with(self, meta_column: MetaColumn):
        meta_column.generator_setting = self._generator_setting
