from __future__ import annotations

import datetime
import random
import string
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Dict, Union

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source import SourceDataProvider
from core.service.data_source.database import DatabaseSourceProvider
from core.service.generator import GeneratedDatabase, ColumnGeneratorParamList, ColumnGeneratorParam

OutputType = TypeVar('OutputType')


class ColumnGeneratorBase(Generic[OutputType], ABC):
    name: str
    has_generated_value: bool = True
    has_preview_value: bool = True
    param_list: ColumnGeneratorParamList = []

    ParamValue = Union[str, int, bool]
    ParamDict = Dict[str, ParamValue]

    def __init__(self,
                 meta_table: MetaTable,
                 meta_column: MetaColumn,
                 generated_database: GeneratedDatabase):
        # TODO meta table is useless
        self._meta_table: MetaTable = meta_table
        self._meta_column: MetaColumn = meta_column
        self._generated_database: GeneratedDatabase = generated_database
        self._meta_column.generator_params = self._prepare_params()

    @classmethod
    def _convert_param_value(cls, param: ColumnGeneratorParam, value) -> ParamValue:
        if param.value_type == 'number' and not isinstance(value, int):
            return int(value)
        if param.value_type == 'bool' and not isinstance(value, bool):
            return value == 'true'
        return value

    def _prepare_params(self) -> ParamDict:
        result = {}
        for param in self.param_list:
            if self._meta_column.generator_params and \
               param.name in self._meta_column.generator_params:
                value = self._meta_column.generator_params[param.name]
                converted = self._convert_param_value(param, value)
                result[param.name] = converted
            else:
                result[param.name] = param.default_value
        return result

    @property
    def _params(self) -> dict:
        return self._meta_column.generator_params

    @classmethod
    @abstractmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return False

    def make_value(self) -> OutputType:
        pass

    def make_preview_value(self) -> OutputType:
        return self.make_value()

    def estimate_params(self):
        data_source = self._meta_column.data_source
        if data_source is None:
            raise Exception('cannot estimate parameters without a data source')
        # TODO choose appropriate provider
        provider = DatabaseSourceProvider(data_source, self._meta_column.reflected_column_idf)
        self._estimate_params_with_provider(provider)

    def _estimate_params_with_provider(self, provider: SourceDataProvider):
        pass


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

    def estimate_params_with_provider(self, provider: SourceDataProvider):
        self._params['from'] = provider.estimate_min() or self.param_list[0].default_value
        self._params['to'] = provider.estimate_max() or self.param_list[1].default_value


class DatetimeGenerator(ColumnGeneratorBase[int]):
    name = 'datetime'

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'DATETIME'

    def make_value(self) -> datetime.datetime:
        return datetime.datetime.now()
