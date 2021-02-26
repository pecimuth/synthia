import random

from core.model.meta_column import MetaColumn
from core.service.column_generator import ColumnGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class BernoulliGenerator(ColumnGenerator[bool]):
    name = 'bernoulli'
    param_list = [
        ColumnGeneratorParam(
            name='success_probability',
            value_type=Types.FLOAT,
            min_value=0.0,
            max_value=1.0,
            default_value=0.5
        )
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == Types.BOOL

    def make_scalar(self, generated_database: GeneratedDatabase) -> bool:
        return random.random() <= self._params['success_probability']

    def _estimate_params_with_provider(self, provider: DataProvider):
        samples = 2
        successes = 1
        for sample in provider.scalar_data():
            if sample is None:
                continue
            samples += 1
            successes += bool(sample)
        self._params['success_probability'] = successes / samples
