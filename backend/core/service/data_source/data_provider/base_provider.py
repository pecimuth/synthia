from abc import ABC, abstractmethod
from functools import reduce
from itertools import islice

from typing import Iterator, Callable, Any, Tuple, Optional

from core.model.data_source import DataSource
from core.service.data_source.identifier import Identifiers
from core.service.injector import Injector

DEFAULT_ROW_LIMIT = 100


class DataProvider(ABC):
    """Provide data from a data source."""

    def __init__(self, data_source: DataSource, identifiers: Identifiers, injector: Injector):
        self._data_source = data_source
        self._identifiers = identifiers
        self._injector = injector

    @abstractmethod
    def scalar_data(self) -> Iterator[Any]:
        """Return scalar data.

        Most useful for single-column generators.
        Return values identified by the first element in the list of identifies.
        """
        pass

    @abstractmethod
    def vector_data(self) -> Iterator[Tuple]:
        """Return vector data.

        Most useful for multi-column generators.
        Return tuples of values in order of identifiers.
        """
        pass

    def scalar_data_not_none(self) -> Iterator[Any]:
        """Return scalar data without None values."""
        for sample in self.scalar_data():
            if sample is not None:
                yield sample

    def reduce(self, function: Callable, initial: Any, limit=DEFAULT_ROW_LIMIT) -> Any:
        """Reduce on the first limit scalar entries."""
        return reduce(
            function,
            islice(self.scalar_data(), 0, limit),
            initial
        )

    def reduce_not_none(self, function: Callable, initial: Any, limit=DEFAULT_ROW_LIMIT) -> Any:
        """Reduce on the first limit non-null scalar entries."""
        return reduce(
            function,
            islice(self.scalar_data_not_none(), 0, limit),
            initial
        )

    def estimate_min(self):
        """Return minimum scalar value or None in case there are no values."""
        def safe_min(seq, elem):
            if seq is None:
                return elem
            return min(seq, elem)
        return self.reduce_not_none(safe_min, None)

    def estimate_max(self):
        """Return maximum scalar value or None in case there are no values."""
        def safe_max(seq, elem):
            if seq is None:
                return elem
            return max(seq, elem)
        return self.reduce_not_none(safe_max, None)

    def get_count(self) -> int:
        """Return number of scalar entries."""
        return self.reduce(lambda x, _: x + 1, 0)

    def get_null_count(self):
        """Return number of None scalar entries."""
        def count_nulls(seq, elem):
            if elem is None:
                return seq + 1
            return seq
        return self.reduce(count_nulls, 0)

    def estimate_null_frequency(self) -> Optional[float]:
        """Return frequency of None values in scalar entries or None."""
        count = self.get_count()
        if count == 0:
            return None
        nulls = self.get_null_count()
        return nulls / count

    def estimate_mean(self) -> Optional[float]:
        """Return mean scalar value or None."""
        sample_sum = 0
        count = 0
        for sample in self.scalar_data_not_none():
            count += 1
            sample_sum += sample
        if count == 0:
            return None
        return sample_sum / count

    def estimate_variance(self) -> Optional[float]:
        """Return an estimate of scalar values or None."""
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
