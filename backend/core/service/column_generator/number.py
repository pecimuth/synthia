import random

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class IntegerGenerator(ColumnGenerator[int]):
    name = 'integer'
    only_for_type = Types.INTEGER
    param_list = [
        ColumnGeneratorParam(
            name='min',
            value_type=Types.INTEGER,
            default_value=-100
        ),
        ColumnGeneratorParam(
            name='max',
            value_type=Types.INTEGER,
            default_value=100,
            greater_equal_than='min'
        )
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == Types.INTEGER

    def make_scalar(self, generated_database: GeneratedDatabase) -> int:
        return random.randint(self._params['min'], self._params['max'])

    def _estimate_params_with_provider(self, provider: DataProvider):
        self._params['min'] = provider.estimate_min() or self.param_list[0].default_value
        self._params['max'] = provider.estimate_max() or self.param_list[1].default_value


class FloatGenerator(ColumnGenerator[float]):
    name = 'float'
    only_for_type = Types.FLOAT
    param_list = [
        ColumnGeneratorParam(
            name='min',
            value_type=Types.FLOAT,
            default_value=-1.
        ),
        ColumnGeneratorParam(
            name='max',
            value_type=Types.FLOAT,
            default_value=1.,
            greater_equal_than='min'
        )
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == Types.FLOAT

    def make_scalar(self, generated_database: GeneratedDatabase) -> float:
        return random.uniform(self._params['min'], self._params['max'])

    def _estimate_params_with_provider(self, provider: DataProvider):
        self._params['min'] = float(provider.estimate_min()) or self.param_list[0].default_value
        self._params['max'] = float(provider.estimate_max()) or self.param_list[1].default_value
