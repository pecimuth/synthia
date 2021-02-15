from abc import ABC, abstractmethod
from functools import reduce

from typing import List, Iterator, Union, Callable, Any

from core.model.data_source import DataSource


class DataProvider(ABC):
    def __init__(self, data_source: DataSource, idf: Union[str, None]):
        self._data_source = data_source
        self._idf = idf

    @abstractmethod
    def identifiers(self) -> List[str]:
        pass

    @abstractmethod
    def column_data(self) -> Iterator:
        pass

    def reduce(self, function: Callable, initial: Any) -> Any:
        # TODO generic types
        return reduce(function, self.column_data(), initial)

    def estimate_min(self):
        def safe_min(seq, elem):
            return elem if seq is None else min(seq, elem)
        return self.reduce(safe_min, None)

    def estimate_max(self):
        def safe_max(seq, elem):
            return elem if seq is None else max(seq, elem)
        return self.reduce(safe_max, None)
