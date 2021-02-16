import json
from typing import Iterator

from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.exception import DataSourceIdentifierError


class JsonDataProvider(DataProvider):
    def column_data(self) -> Iterator:
        with open(self._data_source.file_path) as file:
            obj = json.loads(file.read())
            table = obj
            if isinstance(obj, dict):
                if self._idf.table not in obj:
                    raise DataSourceIdentifierError('table not found', self._data_source, self._idf)
                table = obj[self._idf.table]
            for row in table:
                if self._idf.column not in row:
                    raise DataSourceIdentifierError('column not found', self._data_source, self._idf)
                yield row[self._idf.column]
