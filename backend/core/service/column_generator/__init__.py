from typing import Type, List, Tuple, Union

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import ColumnGeneratorBase, OutputType

from core.service.column_generator import special, datetime, number, string, boolean
from core.service.exception import ColumnGeneratorError


def get_generator_by_name(name: str) -> Type[ColumnGeneratorBase[OutputType]]:
    if not hasattr(get_generator_by_name, 'gen_by_name'):
        get_generator_by_name.gen_by_name = {
            column_gen.name: column_gen
            for column_gen in ColumnGeneratorBase.__subclasses__()
        }
    return get_generator_by_name.gen_by_name[name]


def find_recommended_generator(meta_column: MetaColumn) -> Union[Type[ColumnGeneratorBase], None]:
    for column_gen in ColumnGeneratorBase.__subclasses__():
        if column_gen.only_for_type is not None and \
           column_gen.only_for_type != meta_column.col_type:
            continue
        if column_gen.is_recommended_for(meta_column):
            return column_gen
    return None


def make_generator_instance_for_meta_column(meta_column: MetaColumn) -> ColumnGeneratorBase:
    if meta_column.generator_setting is None:
        generator_factory = find_recommended_generator(meta_column)
        if generator_factory is None:
            raise ColumnGeneratorError('no suitable generator found', meta_column)
        generator_setting = generator_factory.create_setting_instance()
        meta_column.generator_setting = generator_setting
        generator_setting.table = meta_column.table
        if meta_column.nullable:
            generator_setting.null_frequency = GeneratorSetting.NULL_FREQUENCY_DEFAULT
        else:
            generator_setting.null_frequency = 0
    else:
        generator_factory = get_generator_by_name(meta_column.generator_setting.name)
        if generator_factory is None:
            raise ColumnGeneratorError('invalid generator name', meta_column)
    return generator_factory(meta_column.generator_setting)


ColumnGeneratorPairs = List[Tuple[MetaColumn, ColumnGeneratorBase]]


def make_generator_instances_for_table(meta_table: MetaTable) -> ColumnGeneratorPairs:
    pairs = []
    for meta_column in meta_table.columns:
        generator_instance = make_generator_instance_for_meta_column(meta_column)
        pairs.append((meta_column, generator_instance))
    return pairs
