import os
from abc import ABC, abstractmethod
from functools import reduce

from typing import List, Iterator, Union, Callable, Any

from core.model.data_source import DataSource
from core.model.project import Project


class SourceDataProvider(ABC):
    def __init__(self, data_source: DataSource, idf: Union[str, None]):
        self._data_source = data_source
        self._idf = idf

    @abstractmethod
    def test_connection(self) -> bool:
        pass

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


class DataSourceUtil:
    EXT_CSV = 'csv'
    EXT_JSON = 'json'
    EXT_SQLITE = ['db', 'sql', 'sqlite', 'sqlite3']

    MIME_TYPE_CSV = 'text/csv'
    MIME_TYPE_JSON = 'application/json'
    MIME_TYPE_SQLITE = 'application/vnd.sqlite3'

    DRIVER_SQLITE = 'sqlite'
    DRIVER_POSTGRES = 'postgresql'

    def __init__(self, proj: Project, storage_root: str):
        self._proj = proj
        self._storage_root = storage_root

    @classmethod
    def is_file_allowed(cls, file_name: str) -> bool:
        if '.' not in file_name:
            return False
        ext = cls._extension(file_name)
        return ext in [cls.EXT_CSV, cls.EXT_JSON] or ext in cls.EXT_SQLITE

    @classmethod
    def _extension(cls, file_name: str) -> str:
        return file_name.rsplit('.', 1)[1].lower()

    @classmethod
    def _extension_to_mime_type(cls, extension: str) -> str:
        if extension == cls.EXT_CSV:
            return cls.MIME_TYPE_CSV
        elif extension == cls.EXT_JSON:
            return cls.MIME_TYPE_JSON
        elif extension in cls.EXT_SQLITE:
            return cls.MIME_TYPE_SQLITE
        raise Exception('unsupported file extension')

    def make_file_path(self, file_name: str):
        return os.path.join(self._storage_root, self._proj.id, file_name)

    def create_file_data_source(self, file_name: str) -> DataSource:
        ext = self._extension(file_name)
        data_source = DataSource(
            file_name=file_name,
            mime_type=self._extension_to_mime_type(ext),
            project=self._proj
        )
        if ext == self.EXT_SQLITE:
            data_source.driver = self.DRIVER_SQLITE
            data_source.db = self.make_file_path(file_name)
        return data_source
