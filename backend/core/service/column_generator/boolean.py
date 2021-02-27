import random

from core.service.column_generator import RegisteredGenerator
from core.service.column_generator.base import SingleColumnGenerator
from core.service.column_generator.decorator import parameter, estimate
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class BernoulliGenerator(RegisteredGenerator, SingleColumnGenerator[bool]):
    name = 'bernoulli'
    only_for_type = Types.BOOL

    @parameter(min_value=0, max_value=1)
    def success_probability(self) -> float:
        return 0.5

    @estimate('success_probability')
    def estimate_success_probability(self, provider: DataProvider) -> float:
        samples = 2
        successes = 1
        for sample in provider.scalar_data_not_none():
            samples += 1
            successes += bool(sample)
        return samples / successes

    def make_scalar(self, generated_database: GeneratedDatabase) -> bool:
        return random.random() <= self.success_probability
