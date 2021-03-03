from typing import Type, Iterable, List, Union

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import RegisteredGenerator, ColumnGenerator, MultiColumnGenerator
from core.service.column_generator.setting_facade import GeneratorSettingFacade
from core.service.exception import ColumnGeneratorError


class GeneratorAssignment:
    def __init__(self, meta_table: MetaTable):
        self._meta_table = meta_table
        self._instances: List[ColumnGenerator] = []
        self._multi: List[MultiColumnGenerator] = []

    @classmethod
    def _type_matches(cls,
                      column_gen: Union[Type[ColumnGenerator], ColumnGenerator],
                      col_type: str) -> bool:
        return column_gen.only_for_type() is None or column_gen.only_for_type() == col_type

    @classmethod
    def _generators_for_type(cls, col_type: str) -> Iterable[Type[ColumnGenerator]]:
        for column_gen in RegisteredGenerator.iter():
            if cls._type_matches(column_gen, col_type):
                yield column_gen

    @classmethod
    def _find_for_single_column(cls, meta_column: MetaColumn) -> Type[ColumnGenerator]:
        for column_gen in cls._generators_for_type(meta_column.col_type):
            if column_gen.is_recommended_for(meta_column):
                return column_gen
        raise ColumnGeneratorError('no suitable generator found', meta_column)

    @classmethod
    def maybe_assign(cls, generator_setting: GeneratorSetting, meta_column: MetaColumn) -> bool:
        facade = GeneratorSettingFacade(generator_setting)
        column_gen = facade.make_generator_instance()
        if not cls._assignment_allowed(column_gen, generator_setting, meta_column):
            return False
        meta_column.generator_setting = generator_setting
        if isinstance(column_gen, MultiColumnGenerator):
            column_gen.unite_with(meta_column)
        return True

    @classmethod
    def _assignment_allowed(cls,
                            column_gen: ColumnGenerator,
                            generator_setting: GeneratorSetting,
                            meta_column: MetaColumn) -> bool:
        if not cls._type_matches(column_gen, meta_column):
            return False
        if generator_setting.columns:
            return column_gen.is_multi_column
        return True

    def _maybe_unite(self, factory: Type[ColumnGenerator], meta_column: MetaColumn) -> bool:
        if not factory.is_multi_column or not issubclass(factory, MultiColumnGenerator):
            return False
        for multi_gen in self._multi:
            if multi_gen.name == factory.name and multi_gen.should_unite_with(meta_column):
                multi_gen.unite_with(meta_column)
                return True
        return False

    def assign(self) -> List[ColumnGenerator]:
        self._instances.clear()
        self._multi.clear()
        for meta_column in self._meta_table.columns:
            factory = self._find_for_single_column(meta_column)
            if self._maybe_unite(factory, meta_column):
                continue
            facade = GeneratorSettingFacade.from_meta_column(meta_column, factory)
            instance = facade.make_generator_instance()
            self._instances.append(instance)
        return self._instances
