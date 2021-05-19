from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum
from inspect import signature
from typing import List, Dict, Generic, TypeVar, Optional, Callable, Any, Type, Iterable

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.column_generator.params import normalized_params, ColumnGeneratorParamList
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.exception import GeneratorSettingError, GeneratorRegistrationError, SomeError
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import class_to_types, Types

OutputType = TypeVar('OutputType')
"""Type variable representing the type returned by a column generator."""

OutputDict = Dict[str, Optional[OutputType]]
"""Output type of a (multi column) generator. Keys are column names."""


class GeneratorCategory(Enum):
    """Taxonomy of generators, used in the frontend."""

    GENERAL = 'General'
    ADDRESS = 'Address'
    PERSON = 'Person'
    DATETIME = 'Date & Time'
    TEXT = 'Text'


class ColumnGenerator(Generic[OutputType], ABC):
    """Base column generator.

    Should not be used directly. Generators should derive from the SingleColumnGenerator
    or MultiColumnGenerator classes.
    """

    category: GeneratorCategory = GeneratorCategory.GENERAL
    is_database_generated = False
    """In case of an interactive driver, should the value
    be generated by the output driver?
    
    Only used in special cases, like surrogate key generator.
    """
    supports_null: bool
    """Should nulls be handled automatically?
    
    If set to true, null frequency is read from the input data source.
    Nulls are then generated with that probability (= frequency).
    """

    # for decorator implementation
    param_list: ColumnGeneratorParamList = []
    """List of parameter definitions.
    
    Automatically set by the parameter decorators.
    """

    estimator_list: List[Callable[[ColumnGenerator, DataProvider], Any]] = []
    """List of parameter estimators.
    
    Automatically set by the parameter decorators.
    """

    def __init__(self, generator_setting: GeneratorSetting):
        assert generator_setting.name == self.name()
        self._random = random.Random()
        self._generator_setting = generator_setting
        # normalize the params in case the parameter definitions have changed
        # in order to avoid deadlocks, we should not persist the new object
        self.params = normalized_params(self, self.param_list, self._generator_setting.params)

    @classmethod
    def name(cls):
        """Return the generator name. Comes from the class name by default."""
        cls_name: str = cls.__name__
        suffix = 'Generator'
        if cls_name.endswith(suffix):
            return cls_name[:-len(suffix)]
        return cls_name

    @classmethod
    @abstractmethod
    def only_for_type(cls) -> Optional[Types]:
        """Return for which type is the generator appropriate.
        It will not be possible to assign it to column of other type.

        Return value of None means any type.
        """
        pass

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        """Return whether the generator should be matched with the column
        by default.
        """
        pass

    def seed(self, seed: Optional[float]):
        """Set random seed."""
        self._random.seed(seed)

    @abstractmethod
    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        """Generate and return the data for assigned columns.

        Generated database contains each previously generated row.
        The output dictionary must contain exactly the keys of assigned column names.
        """
        pass

    @classmethod
    def create_setting_instance(cls) -> GeneratorSetting:
        """Return a new setting instance of this generator type."""
        return GeneratorSetting(name=cls.name())

    @property
    def setting(self) -> GeneratorSetting:
        """Return the setting instance assigned to this generator instance."""
        return self._generator_setting

    def save_params(self, normalize: bool = False):
        """Save the current parameters to the generator setting. If normalize is True,
        the parameters are also normalized according to the definitions."""
        if normalize:
            self.params = normalized_params(self, self.param_list, self.params)
        self._generator_setting.params = self.params

    @property
    def _meta_columns(self) -> List[MetaColumn]:
        """Return list of assigned columns."""
        return self._generator_setting.columns

    def estimate_params(self, provider: DataProvider):
        """Estimate the generator params with the given provider.

        In case the generator supports nulls, null frequency is estimated.
        After that, estimators are called. The method does not update
        the generator setting instance. Estimated parameters may not adhere
        to the parameter definitions - normalization is needed.
        """
        if self.supports_null:
            estimate = provider.estimate_null_frequency()
            if estimate is not None:
                self._generator_setting.null_frequency = estimate
        for estimator in self.estimator_list:
            estimator(self, provider)


class RegisteredGenerator(ABC):
    """Marks a column generator. Manages the list of column generators.

    Each column generator deriving from this class is automatically
    considered for generator assignment and should show up in the frontend.
    """

    _by_name: Optional[Dict[str, Type[ColumnGenerator]]] = None
    """Column generator types by generator name."""

    @classmethod
    def _make_dict(cls):
        """Prepare dictionary of generators by name."""
        cls._by_name = {}
        for column_gen in RegisteredGenerator.__subclasses__():
            if not issubclass(column_gen, ColumnGenerator):
                raise GeneratorRegistrationError()
            cls._by_name[column_gen.name()] = column_gen

    @classmethod
    def _require_dict(cls):
        """Make sure that we have the generator dictionary."""
        if cls._by_name is None:
            cls._make_dict()

    @classmethod
    def is_name_registered(cls, name: str) -> bool:
        """Return whether the name is a registered generator name."""
        cls._require_dict()
        return name in cls._by_name

    @classmethod
    def get_by_name(cls, name: str) -> Type[ColumnGenerator[OutputType]]:
        """Return generator type by name."""
        if not cls.is_name_registered(name):
            raise SomeError('invalid generator name')
        return cls._by_name[name]

    @classmethod
    def iter(cls) -> Iterable[Type[ColumnGenerator]]:
        """Return iterator of generator types."""
        cls._require_dict()
        return cls._by_name.values()


class SingleColumnGenerator(Generic[OutputType], ColumnGenerator[OutputType]):
    """Base class for single column generators."""

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
        """Return supported type.

        The type is read from the make_scalar return annotation.
        """
        sig = signature(cls.make_scalar)
        klass = sig.return_annotation
        if not isinstance(klass, TypeVar):
            return class_to_types(klass)
        return None

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        """Return whether the column name matches generator name."""
        return cls.name().lower() in meta_column.name.replace('_', '').lower()

    @property
    def _null_frequency(self) -> float:
        """Return the frequency of None values in generator output."""
        return self._generator_setting.null_frequency

    @property
    def _meta_column(self) -> MetaColumn:
        """Return the single assigned column."""
        return self._generator_setting.columns[0]

    @abstractmethod
    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        """Return generated value.

        This method should be used by most implemented generators.
        It should not return None. None will be automatically generated
        by the make_scalar_or_null method.
        """
        pass

    def make_scalar_or_null(self, generated_database: GeneratedDatabase) -> Optional[OutputType]:
        """Return generated value or None (in case supports_null is True).

        In case supports_null is False, make_scalar is called only.
        None is returned with probability of null_frequency,
        make_scalar is called with probability (1 - null_frequency)
        """
        if self.supports_null and self._random.random() < self._null_frequency:
            return None
        return self.make_scalar(generated_database)

    def make_dict(self, generated_database: GeneratedDatabase) -> OutputDict:
        return {
            meta_column.name: self.make_scalar_or_null(generated_database)
            for meta_column in self._meta_columns
        }


class MultiColumnGenerator(Generic[OutputType], ColumnGenerator[OutputType], ABC):
    """Base class for multi column generators."""

    supports_null = False

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return None

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def should_unite_with(self, meta_column: MetaColumn) -> bool:
        """Should the generator instance be automatically united with the column?"""
        return False

    def unite_with(self, meta_column: MetaColumn):
        """Assign the column to the generator setting."""
        meta_column.generator_setting = self._generator_setting
