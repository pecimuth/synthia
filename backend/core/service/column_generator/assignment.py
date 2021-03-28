from typing import Type, Iterable, List, Union

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import RegisteredGenerator, ColumnGenerator, MultiColumnGenerator
from core.service.column_generator.setting_facade import GeneratorSettingFacade
from core.service.exception import ColumnGeneratorError


class GeneratorAssignment:
    """Utility class providing generator (setting) to column assignment."""

    def __init__(self, meta_table: MetaTable):
        self._meta_table = meta_table
        self._instances: List[ColumnGenerator] = []
        self._multi: List[MultiColumnGenerator] = []

    @classmethod
    def _type_matches(cls,
                      column_gen: Union[Type[ColumnGenerator], ColumnGenerator],
                      col_type: str) -> bool:
        """Return whether a generator instance/type is compatible with column type."""
        return column_gen.only_for_type() is None or column_gen.only_for_type() == col_type

    @classmethod
    def _generators_for_type(cls, col_type: str) -> Iterable[Type[ColumnGenerator]]:
        """Return an iterable of generators compatible with given type."""
        for column_gen in RegisteredGenerator.iter():
            if cls._type_matches(column_gen, col_type):
                yield column_gen

    @classmethod
    def _find_for_single_column(cls, meta_column: MetaColumn) -> Type[ColumnGenerator]:
        """Find the recommended generator for a column."""
        for column_gen in cls._generators_for_type(meta_column.col_type):
            if column_gen.is_recommended_for(meta_column):
                return column_gen
        raise ColumnGeneratorError('No suitable generator found', meta_column)

    @classmethod
    def maybe_assign(cls, generator_setting: GeneratorSetting, meta_column: MetaColumn) -> bool:
        """Try to assign a generator to a column and return whether it succeeded.

        We check that the types are compatible and if there are already assigned
        columns, the generator must be multi column.
        """
        facade = GeneratorSettingFacade(generator_setting)
        factory = facade.get_generator_type()
        if not cls._assignment_allowed(factory, generator_setting, meta_column):
            return False
        column_gen = facade.make_generator_instance()
        if isinstance(column_gen, MultiColumnGenerator):
            column_gen.unite_with(meta_column)
        else:
            meta_column.generator_setting = generator_setting
        return True

    @classmethod
    def _assignment_allowed(cls,
                            factory: Type[ColumnGenerator],
                            generator_setting: GeneratorSetting,
                            meta_column: MetaColumn) -> bool:
        """Return whether generator (and its setting) is assignable to a column.

        The types must match. In case there are columns already assignment,
        it must be a multi column generator.
        """
        if not cls._type_matches(factory, meta_column.col_type):
            return False
        if generator_setting.columns:
            return issubclass(factory, MultiColumnGenerator)
        return True

    def _maybe_unite(self, factory: Type[ColumnGenerator], meta_column: MetaColumn) -> bool:
        """Try to unite a column with an existing multi column generator.
        Return whether the column was successfully united.

        Checks whether the factory is multi column and sequentially tries
        each existing instance of the same factory in the current table.
        """
        if not issubclass(factory, MultiColumnGenerator):
            return False
        for multi_gen in self._multi:
            if multi_gen.name == factory.name and multi_gen.should_unite_with(meta_column):
                multi_gen.unite_with(meta_column)
                return True
        return False

    def assign(self) -> List[ColumnGenerator]:
        """Find and assign recommended generators to each column in the table."""
        self._instances.clear()
        self._multi.clear()
        for meta_column in self._meta_table.columns:
            factory = self._find_for_single_column(meta_column)
            if self._maybe_unite(factory, meta_column):
                continue
            facade = GeneratorSettingFacade.from_meta_column(meta_column, factory)
            instance = facade.make_generator_instance()
            if isinstance(instance, MultiColumnGenerator):
                self._multi.append(instance)
            self._instances.append(instance)
        return self._instances
