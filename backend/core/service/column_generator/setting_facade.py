from __future__ import annotations

import random
from typing import List, Type

from sqlalchemy.orm.attributes import flag_modified

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import ColumnGenerator, RegisteredGenerator

from core.service.data_source.data_provider import DataProviderFactory
from core.service.injector import Injector

GeneratorList = List[ColumnGenerator]
"""List of column generator instances."""


class GeneratorSettingFacade:
    """Provides utility functions related to generator settings."""

    def __init__(self, generator_setting: GeneratorSetting):
        self._generator_setting = generator_setting

    @classmethod
    def from_meta_column(cls,
                         meta_column: MetaColumn,
                         factory: Type[ColumnGenerator] = None) -> GeneratorSettingFacade:
        generator_setting = meta_column.generator_setting
        if generator_setting is None:
            if factory is None:
                raise ValueError('generator factory must not be none')
            generator_setting = cls._create_generator_setting(meta_column, factory)
        return GeneratorSettingFacade(generator_setting)

    @staticmethod
    def instances_from_table(meta_table: MetaTable) -> GeneratorList:
        """Make generator instances for generator settings in a table."""
        instances = []
        for generator_setting in meta_table.generator_settings:
            if not generator_setting.columns:
                continue
            facade = GeneratorSettingFacade(generator_setting)
            instance = facade.make_generator_instance()
            instances.append(instance)
        return instances

    @staticmethod
    def seed_all(instances: GeneratorList, seed: int):
        """Seed all generator instances in a list with a random seed,
        influenced by the input seed."""
        random_inst = random.Random(seed)
        for instance in instances:
            instance.seed(random_inst.random())

    @classmethod
    def _create_generator_setting(cls,
                                  meta_column: MetaColumn,
                                  factory: Type[ColumnGenerator]) -> GeneratorSetting:
        """Create a generator setting of given type and assign it to a column."""
        generator_setting = factory.create_setting_instance()
        meta_column.generator_setting = generator_setting
        generator_setting.table = meta_column.table
        if meta_column.nullable:
            generator_setting.null_frequency = GeneratorSetting.NULL_FREQUENCY_DEFAULT
        else:
            generator_setting.null_frequency = 0
        return generator_setting

    def make_generator_instance(self) -> ColumnGenerator:
        """Create and return an instance of the generator."""
        generator_factory = RegisteredGenerator.get_by_name(self._generator_setting.name)
        return generator_factory(self._generator_setting)

    def maybe_estimate_params(self, injector: Injector):
        """Estimate the generator (setting) params in case a data source is available."""
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
