from math import sqrt
from typing import Optional

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
        return self._random.randint(self.min, self.max)

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
        return self._random.uniform(self.min, self.max)


class GaussianGenerator(RegisteredGenerator, SingleColumnGenerator[float]):

    @parameter
    def mu(self) -> float:
        return 0.

    @parameter(min_value=0)
    def sigma(self) -> float:
        return 1.

    @mu.estimator
    def mu(self, provider: DataProvider) -> Optional[float]:
        return provider.estimate_mean()

    @sigma.estimator
    def sigma(self, provider: DataProvider) -> Optional[float]:
        variance = provider.estimate_variance()
        if variance is None:
            return None
        return sqrt(variance)

    def make_scalar(self, generated_database: GeneratedDatabase) -> float:
        return self._random.gauss(self.mu, self.sigma)
