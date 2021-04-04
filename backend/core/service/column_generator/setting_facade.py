from __future__ import annotations

from typing import List, Type

from sqlalchemy.orm.attributes import flag_modified

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGenerator, RegisteredGenerator

from core.service.data_source.data_provider import DataProviderFactory
from core.service.injector import Injector

GeneratorList = List[ColumnGenerator]
"""List of column generator instances."""


class GeneratorSettingFacade:
    """Provides generator setting creation, parameter estimation
    and generator instance creation.

    An instance can be created from a generator setting
    or from a column, which gets a new setting assigned.
    """

    def __init__(self, generator_setting: GeneratorSetting):
        self._generator_setting = generator_setting

    @staticmethod
    def with_new_setting(meta_column: MetaColumn, factory: Type[ColumnGenerator]) -> GeneratorSettingFacade:
        """Create a generator setting of given type and assign it to a column.
        Return a facade instance.
        """
        generator_setting = factory.create_setting_instance()
        meta_column.generator_setting = generator_setting
        generator_setting.table = meta_column.table
        if meta_column.nullable:
            generator_setting.null_frequency = GeneratorSetting.NULL_FREQUENCY_DEFAULT
        else:
            generator_setting.null_frequency = 0
        return GeneratorSettingFacade(generator_setting)

    def make_generator_instance(self) -> ColumnGenerator:
        """Create and return an instance of the generator."""
        factory = RegisteredGenerator.get_by_name(self._generator_setting.name)
        return factory(self._generator_setting)

    def maybe_estimate_params(self, injector: Injector):
        """Estimate the generator (setting) params in case a data source is available.

        The generator parameters are normalized in either case.
        """
        gen_instance = self.make_generator_instance()  # normalizes params
        if not self._has_data_source():
            return
        self.estimate_params(gen_instance, injector)

    def estimate_params(self, gen_instance: ColumnGenerator, injector: Injector):
        """Estimate parameters for the generator instance."""
        factory = DataProviderFactory(self._generator_setting.columns, injector)
        provider = factory.find_provider()
        gen_instance.estimate_params(provider)
        flag_modified(self._generator_setting, 'params')  # register the param change

    def _has_data_source(self) -> bool:
        """Return whether any of the assigned column has a data source defined."""
        for meta_column in self._generator_setting.columns:
            if meta_column.data_source is not None:
                return True
        return False
