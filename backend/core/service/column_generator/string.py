import random
import string

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class StringGenerator(ColumnGenerator[str]):
    name = 'string'
    only_for_type = Types.STRING
    param_list = [
        ColumnGeneratorParam(
            name='min_length',
            value_type=Types.INTEGER,
            default_value=1,
            min_value=1
        ),
        ColumnGeneratorParam(
            name='max_length',
            value_type=Types.INTEGER,
            default_value=10,
            max_value=100,
            greater_equal_than='min_length'
        )
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == Types.STRING

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        length = random.randint(self._params['min_length'], self._params['max_length'])
        return self._random_string_of_length(length)

    @classmethod
    def _random_string_of_length(cls, length: int) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def _estimate_params_with_provider(self, provider: DataProvider):
        min_len = None
        max_len = None
        for sample in provider.scalar_data():
            if sample is None:
                continue
            if min_len is None or len(sample) < min_len:
                min_len = len(sample)
            if max_len is None or len(sample) > max_len:
                max_len = len(sample)
        self._params['min_length'] = min_len or self.param_list[0].default_value
        self._params['max_length'] = max_len or self.param_list[1].default_value
