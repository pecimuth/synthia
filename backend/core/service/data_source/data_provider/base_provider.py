from abc import ABC, abstractmethod
from functools import reduce
from itertools import islice

from typing import Iterator, Callable, Any, Tuple, Union

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

    def reduce(self, function: Callable, initial: Any, limit=DEFAULT_ROW_LIMIT) -> Any:
        # TODO generic types
        return reduce(
            function,
            islice(self.scalar_data(), 0, limit),
            initial
        )

    def estimate_min(self, limit=DEFAULT_ROW_LIMIT):
        def safe_min(elem, seq):
            if elem is None:
                return seq
            if seq is None:
                return elem
            return min(seq, elem)
        return self.reduce(safe_min, None, limit)

    def estimate_max(self, limit=DEFAULT_ROW_LIMIT):
        def safe_max(elem, seq):
            if elem is None:
                return seq
            if seq is None:
                return elem
            return max(seq, elem)
        return self.reduce(safe_max, None, limit)

    def estimate_null_frequency(self, limit=DEFAULT_ROW_LIMIT) -> Union[float, None]:
        nulls = 0
        samples = 0
        for sample in islice(self.scalar_data(), 0, limit):
            nulls += sample is None
            samples += 1
        if samples > 0:
            return nulls / samples
        return None
