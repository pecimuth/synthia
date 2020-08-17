from __future__ import annotations

import datetime
import random
import string
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Dict, Union

from app.model.meta_column import MetaColumn
from app.model.meta_table import MetaTable
from app.service.generator import GeneratedDatabase, ColumnGeneratorParamList, ColumnGeneratorParam

OutputType = TypeVar('OutputType')


class ColumnGeneratorBase(Generic[OutputType], ABC):
    name: str
    has_generated_value: bool = True
    has_preview_value: bool = True
    param_list: ColumnGeneratorParamList = []

    def __init__(self,
                 meta_table: MetaTable,
                 meta_column: MetaColumn,
                 generated_database: GeneratedDatabase):
        self._meta_table: MetaTable = meta_table
        self._meta_column: MetaColumn = meta_column
        self._generated_database: GeneratedDatabase = generated_database
        self._params = self._prepare_params()

    def _prepare_params(self) -> Dict[str, Union[str, int, bool]]:
        result = {}
        for param in self.param_list:
            if self._meta_column.generator_params and \
               param.name in self._meta_column.generator_params:
                result[param.name] = self._meta_column.generator_params[param.name]
            else:
                result[param.name] = param.default_value
        return result

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def make_value(self) -> OutputType:
        pass

    def make_preview_value(self) -> OutputType:
        return self.make_value()


def find_recommended_generator(meta_column: MetaColumn) -> Type[ColumnGeneratorBase[OutputType]]:
    for column_gen in ColumnGeneratorBase.__subclasses__():
        if column_gen.is_recommended_for(meta_column):
            return column_gen


def get_generator_by_name(name: str) -> Type[ColumnGeneratorBase[OutputType]]:
    if not hasattr(get_generator_by_name, 'gen_by_name'):
        get_generator_by_name.gen_by_name = {
            column_gen.name : column_gen
            for column_gen in ColumnGeneratorBase.__subclasses__()
        }
    return get_generator_by_name.gen_by_name[name]


class PrimaryKeyGenerator(ColumnGeneratorBase[None]):
    name = 'primary_key'
    has_generated_value = False
    has_preview_value = False

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.primary_key and meta_column.col_type == 'INTEGER'


class ForeignKeyGenerator(ColumnGeneratorBase[int]):
    name = 'foreign_key'
    has_preview_value = False

    def __init__(self,
                 meta_table: MetaTable,
                 meta_column: MetaColumn,
                 generated_database: GeneratedDatabase):
        super().__init__(meta_table, meta_column, generated_database)
        foreign_key = meta_column.foreign_key.split('.')
        assert len(foreign_key) >= 2
        self._fk_column_name = foreign_key[-1]
        self._fk_table_name = foreign_key[-2]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.foreign_key and meta_column.col_type == 'INTEGER'

    def make_value(self) -> int:
        row = random.choice(self._generated_database[self._fk_table_name])
        return row[self._fk_column_name]


class StringGenerator(ColumnGeneratorBase[str]):
    name = 'string'
    param_list = [
        ColumnGeneratorParam(name='length', value_type='number', default_value=10)
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'VARCHAR'

    def make_value(self) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(self._params['length']))


class IntegerGenerator(ColumnGeneratorBase[int]):
    name = 'integer'
    param_list = [
        ColumnGeneratorParam(name='from', value_type='number', default_value=0),
        ColumnGeneratorParam(name='to', value_type='number', default_value=1000000)
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'INTEGER'

    def make_value(self) -> int:
        return random.randint(self._params['from'], self._params['to'])


class DatetimeGenerator(ColumnGeneratorBase[int]):
    name = 'datetime'

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'DATETIME'

    def make_value(self) -> datetime.datetime:
        return datetime.datetime.now()
