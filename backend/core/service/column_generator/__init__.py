from __future__ import annotations

from typing import Type, List

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import ColumnGenerator, OutputType, RegisteredGenerator

import core.service.column_generator.faker_generator
import core.service.column_generator.basic_generator
from core.service.data_source.data_provider import DataProviderFactory
from core.service.exception import ColumnGeneratorError

GeneratorList = List[ColumnGenerator]


class GeneratorSettingFacade:
    def __init__(self, generator_setting: GeneratorSetting):
        self._generator_setting = generator_setting

    @classmethod
    def from_meta_column(cls, meta_column: MetaColumn) -> GeneratorSettingFacade:
        generator_setting = meta_column.generator_setting
        if generator_setting is None:
            generator_setting = cls._create_generator_setting(meta_column)
        return GeneratorSettingFacade(generator_setting)

    @staticmethod
    def instances_from_table(meta_table: MetaTable) -> GeneratorList:
        instances = []
        for generator_setting in meta_table.generator_settings:
            if not generator_setting.columns:
                continue
            facade = GeneratorSettingFacade(generator_setting)
            instance = facade.make_generator_instance()
            instances.append(instance)
        return instances

    @classmethod
    def _create_generator_setting(cls, meta_column: MetaColumn) -> GeneratorSetting:
        generator_factory = cls._find_recommended_generator(meta_column)
        generator_setting = generator_factory.create_setting_instance()
        meta_column.generator_setting = generator_setting
        generator_setting.table = meta_column.table
        if meta_column.nullable:
            generator_setting.null_frequency = GeneratorSetting.NULL_FREQUENCY_DEFAULT
        else:
            generator_setting.null_frequency = 0
        return generator_setting

    @classmethod
    def _find_recommended_generator(cls, meta_column: MetaColumn) -> Type[ColumnGenerator]:
        for column_gen in RegisteredGenerator.iter():
            if column_gen.only_for_type() is not None and \
               column_gen.only_for_type() != meta_column.col_type:
                continue
            if column_gen.is_recommended_for(meta_column):
                return column_gen
        raise ColumnGeneratorError('no suitable generator found', meta_column)

    def make_generator_instance(self) -> ColumnGenerator:
        generator_factory = RegisteredGenerator.get_by_name(self._generator_setting.name)
        return generator_factory(self._generator_setting)

    def maybe_estimate_params(self):
        gen_instance = self.make_generator_instance()  # normalizes params
        if not self._has_data_source():
            return
        self._estimate_params(gen_instance)

    def _estimate_params(self, gen_instance: ColumnGenerator):
        factory = DataProviderFactory(self._generator_setting.columns)
        provider = factory.find_provider()
        gen_instance.estimate_params(provider)

    def _has_data_source(self) -> bool:
        for meta_column in self._generator_setting.columns:
            if meta_column.data_source is not None:
                return True
        return False
