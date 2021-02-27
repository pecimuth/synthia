import random

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import RegisteredGenerator, SingleColumnGenerator
from core.service.column_generator.decorator import parameter
from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase


class IntegerGenerator(RegisteredGenerator, SingleColumnGenerator[int]):

    @parameter
    def min(self) -> int:
        return -100

    @parameter(greater_equal_than='min')
    def max(self) -> int:
        return 100

    @min.estimator
    def min(self, provider: DataProvider) -> int:
        return provider.estimate_min()

    @max.estimator
    def max(self, provider: DataProvider) -> int:
        return provider.estimate_max()

    def make_scalar(self, generated_database: GeneratedDatabase) -> int:
        return random.randint(self.min, self.max)

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return True


class FloatGenerator(RegisteredGenerator, SingleColumnGenerator[float]):

    @parameter
    def min(self) -> float:
        return -1.

    @parameter(greater_equal_than='min')
    def max(self) -> float:
        return 1.

    @min.estimator
    def min(self, provider: DataProvider) -> float:
        return float(provider.estimate_min())

    @max.estimator
    def max(self, provider: DataProvider) -> float:
        return float(provider.estimate_max())

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return True

    def make_scalar(self, generated_database: GeneratedDatabase) -> float:
        return random.uniform(self.min, self.max)


class GaussianGenerator(RegisteredGenerator, SingleColumnGenerator[float]):

    @parameter
    def mu(self) -> float:
        return 0.

    @parameter(min_value=0)
    def sigma(self) -> float:
        return 1.

    def make_scalar(self, generated_database: GeneratedDatabase) -> float:
        return random.gauss(self.mu, self.sigma)

    def _estimate_params_with_provider(self, provider: DataProvider):
        sample_sum = 0
        square_sum = 0
        samples = 0
        for sample in provider.scalar_data_not_none():
            samples += 1
            sample_sum += sample
            square_sum += sample ** 2
        if samples == 0:
            return
        first_moment = sample_sum / samples
        second_moment = square_sum / samples
        self.mu = first_moment
        self.sigma = max(second_moment - first_moment ** 2, 0)
