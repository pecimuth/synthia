import random

from core.model.meta_column import MetaColumn
from core.service.column_generator import ColumnGeneratorParam
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase


class IntegerGenerator(ColumnGeneratorBase[int]):
    name = 'integer'
    param_list = [
        ColumnGeneratorParam(name='from', value_type='number', default_value=0),
        ColumnGeneratorParam(name='to', value_type='number', default_value=1000000)
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'INTEGER'

    def make_value(self, generated_database: GeneratedDatabase) -> int:
        return random.randint(self._params['from'], self._params['to'])

    def estimate_params_with_provider(self, provider: DataProvider):
        self._params['from'] = provider.estimate_min() or self.param_list[0].default_value
        self._params['to'] = provider.estimate_max() or self.param_list[1].default_value
