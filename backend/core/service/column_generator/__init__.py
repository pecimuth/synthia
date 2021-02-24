from typing import Type, List, Tuple, Union, Dict

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import ColumnGeneratorBase, OutputType

from core.service.column_generator import special, datetime, number, string, boolean
from core.service.exception import ColumnGeneratorError, SomeError


def get_generator_by_name(name: str) -> Type[ColumnGeneratorBase[OutputType]]:
    if not hasattr(get_generator_by_name, 'gen_by_name'):
        get_generator_by_name.gen_by_name = {
            column_gen.name: column_gen
            for column_gen in ColumnGeneratorBase.__subclasses__()
        }
    if name not in get_generator_by_name.gen_by_name:
        raise SomeError('invalid generator name')
    return get_generator_by_name.gen_by_name[name]


def find_recommended_generator(meta_column: MetaColumn) -> Type[ColumnGeneratorBase]:
    for column_gen in ColumnGeneratorBase.__subclasses__():
        if column_gen.only_for_type is not None and \
           column_gen.only_for_type != meta_column.col_type:
            continue
        if column_gen.is_recommended_for(meta_column):
            return column_gen
    raise ColumnGeneratorError('no suitable generator found', meta_column)


def make_generator_instance_for_meta_column(meta_column: MetaColumn) -> ColumnGeneratorBase:
    if meta_column.generator_setting is None:
        generator_factory = find_recommended_generator(meta_column)
        generator_setting = generator_factory.create_setting_instance()
        meta_column.generator_setting = generator_setting
        generator_setting.table = meta_column.table
        if meta_column.nullable:
            generator_setting.null_frequency = GeneratorSetting.NULL_FREQUENCY_DEFAULT
        else:
            generator_setting.null_frequency = 0
    else:
        generator_factory = get_generator_by_name(meta_column.generator_setting.name)
    return generator_factory(meta_column.generator_setting)


GeneratorList = List[ColumnGeneratorBase]


def make_generator_instances_for_table(meta_table: MetaTable) -> GeneratorList:
    instances = []
    for generator_setting in meta_table.generator_settings:
        if not generator_setting.columns:
            continue
        generator_factory = get_generator_by_name(generator_setting.name)
        instance = generator_factory(generator_setting)
        instances.append(instance)
    return instances
