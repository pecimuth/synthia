import csv
from typing import Iterator, Tuple, Any

from core.service.data_source.data_provider.base_provider import DataProvider


class CsvDataProvider(DataProvider):
    def scalar_data(self) -> Iterator[Any]:
        idf = self._identifiers[0]
        with open(self._data_source.file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row[idf.column]

    def vector_data(self) -> Iterator[Tuple]:
        with open(self._data_source.file_path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield (row[idf.column] for idf in self._identifiers)
