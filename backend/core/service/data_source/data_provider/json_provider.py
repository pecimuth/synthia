import json
from typing import Iterator, Tuple, Any

from core.service.data_source.data_provider.base_provider import DataProvider
from core.service.data_source.identifier import Identifier
from core.service.exception import DataSourceIdentifierError, DataSourceError


class JsonDataProvider(DataProvider):
    def scalar_data(self) -> Iterator[Any]:
        idf = self._identifiers[0]
        json_obj = self._parse_json()
        return self._yield_column(json_obj, idf)

    def vector_data(self) -> Iterator[Tuple]:
        json_obj = self._parse_json()
        scalars = (
            self._yield_column(json_obj, idf)
            for idf in self._identifiers
        )
        return zip(scalars)

    def _parse_json(self) -> Any:
        with open(self._data_source.file_path) as file:
            return json.load(file)

    def _yield_column(self, json_obj: Any, idf: Identifier) -> Iterator[Any]:
        if isinstance(json_obj, dict):
            if idf.table not in json_obj:
                raise DataSourceIdentifierError('table not found', self._data_source, repr(idf))
            table = json_obj[idf.table]
        else:
            if not isinstance(json_obj, list):
                raise DataSourceError('malformed json data source', self._data_source)
            table = json_obj
        for row in table:
            if idf.column not in row:
                raise DataSourceIdentifierError('column not found', self._data_source, repr(idf))
            yield row[idf.column]
