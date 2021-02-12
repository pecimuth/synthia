import random

from core.model.meta_column import MetaColumn
from core.service.column_generator import ColumnGeneratorParam
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.data_source import SourceDataProvider
from core.service.output_driver import OutputDriver


class IntegerGenerator(ColumnGeneratorBase[int]):
    name = 'integer'
    param_list = [
        ColumnGeneratorParam(name='from', value_type='number', default_value=0),
        ColumnGeneratorParam(name='to', value_type='number', default_value=1000000)
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'INTEGER'

    def make_value(self, output_driver: OutputDriver) -> int:
        return random.randint(self._params['from'], self._params['to'])

    def estimate_params_with_provider(self, provider: SourceDataProvider):
        self._params['from'] = provider.estimate_min() or self.param_list[0].default_value
        self._params['to'] = provider.estimate_max() or self.param_list[1].default_value
