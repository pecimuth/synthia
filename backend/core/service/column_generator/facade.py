from typing import Type, List, Tuple

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.base import ColumnGeneratorBase, OutputType

from core.service.column_generator import datetime, number, special, string


def find_recommended_generator(meta_column: MetaColumn) -> Type[ColumnGeneratorBase[OutputType]]:
    for column_gen in ColumnGeneratorBase.__subclasses__():
        if column_gen.is_recommended_for(meta_column):
            return column_gen


def get_generator_by_name(name: str) -> Type[ColumnGeneratorBase[OutputType]]:
    if not hasattr(get_generator_by_name, 'gen_by_name'):
        get_generator_by_name.gen_by_name = {
            column_gen.name: column_gen
            for column_gen in ColumnGeneratorBase.__subclasses__()
        }
    return get_generator_by_name.gen_by_name[name]


ColumnGeneratorPairs = List[Tuple[MetaColumn, ColumnGeneratorBase]]


def make_generator_instances_for_table(meta_table: MetaTable) -> ColumnGeneratorPairs:
    pairs = []
    for meta_column in meta_table.columns:
        if meta_column.generator_name is None:
            generator_factory = find_recommended_generator(meta_column)
        else:
            generator_factory = get_generator_by_name(meta_column.generator_name)

        # TODO improve error handling
        if generator_factory is None:
            raise Exception('No suitable generator for {}.{}'. \
                            format(meta_table.name, meta_column.name))
        generator_instance = generator_factory(meta_column)
        pairs.append((meta_column, generator_instance))
    return pairs
