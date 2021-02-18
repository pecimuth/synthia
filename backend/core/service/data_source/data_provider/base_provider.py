from abc import ABC, abstractmethod
from functools import reduce

from typing import Iterator, Callable, Any

from core.model.data_source import DataSource
from core.service.data_source.identifier import Identifier


class DataProvider(ABC):
    def __init__(self, data_source: DataSource, idf: Identifier):
        self._data_source = data_source
        self._idf = idf

    @abstractmethod
    def column_data(self) -> Iterator:
        pass

    def reduce(self, function: Callable, initial: Any) -> Any:
        # TODO generic types
        return reduce(function, self.column_data(), initial)

    def estimate_min(self):
        def safe_min(elem, seq):
            if elem is None:
                return seq
            if seq is None:
                return elem
            return min(seq, elem)
        return self.reduce(safe_min, None)

    def estimate_max(self):
        def safe_max(elem, seq):
            if elem is None:
                return seq
            if seq is None:
                return elem
            return max(seq, elem)
        return self.reduce(safe_max, None)
