import json
from typing import Iterator

from core.service.data_source.data_provider.base_provider import DataProvider


class JsonDataProvider(DataProvider):
    def column_data(self) -> Iterator:
        with open(self._data_source.file_path) as file:
            obj = json.loads(file.read())
            table = obj
            if isinstance(obj, dict):
                table = obj[self._idf.table]
            for row in table:
                yield row[self._idf.column]
