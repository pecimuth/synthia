from abc import ABC, abstractmethod
from functools import reduce
from itertools import islice

from typing import Iterator, Callable, Any, Tuple, Optional

from core.model.data_source import DataSource
from core.service.data_source.identifier import Identifiers

DEFAULT_ROW_LIMIT = 100


class DataProvider(ABC):
    def __init__(self, data_source: DataSource, identifiers: Identifiers):
        self._data_source = data_source
        self._identifiers = identifiers

    @abstractmethod
    def scalar_data(self) -> Iterator[Any]:
        pass

    @abstractmethod
    def vector_data(self) -> Iterator[Tuple]:
        pass

    def scalar_data_not_none(self) -> Iterator[Any]:
        for sample in self.scalar_data():
            if sample is not None:
                yield sample

    def reduce(self, function: Callable, initial: Any, limit=DEFAULT_ROW_LIMIT) -> Any:
        # TODO generic types
        return reduce(
            function,
            islice(self.scalar_data(), 0, limit),
            initial
        )

    def reduce_not_none(self, function: Callable, initial: Any, limit=DEFAULT_ROW_LIMIT) -> Any:
        # TODO generic types
        return reduce(
            function,
            islice(self.scalar_data_not_none(), 0, limit),
            initial
        )

    def estimate_min(self):
        def safe_min(seq, elem):
            if seq is None:
                return elem
            return min(seq, elem)
        return self.reduce_not_none(safe_min, None)

    def estimate_max(self):
        def safe_max(seq, elem):
            if seq is None:
                return elem
            return max(seq, elem)
        return self.reduce_not_none(safe_max, None)

    def get_count(self) -> int:
        return self.reduce(lambda x, _: x + 1, 0)

    def get_null_count(self):
        def count_nulls(seq, elem):
            if elem is None:
                return seq + 1
            return seq
        return self.reduce(count_nulls, 0)

    def estimate_null_frequency(self, ) -> Optional[float]:
        count = self.get_count()
        if count == 0:
            return None
        nulls = self.get_null_count()
        return nulls / count

    def estimate_mean(self) -> Optional[float]:
        sample_sum = 0
        count = 0
        for sample in self.scalar_data_not_none():
            count += 1
            sample_sum += sample
        if count == 0:
            return None
        return sample_sum / count

    def estimate_variance(self) -> Optional[float]:
        sample_sum = 0
        square_sum = 0
        count = 0
        for sample in self.scalar_data_not_none():
            count += 1
            sample_sum += sample
            square_sum += sample ** 2
        if count == 0:
            return None
        mean = sample_sum / count
        return max(square_sum - mean, 0)
