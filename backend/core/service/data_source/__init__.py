import os
from abc import ABC, abstractmethod

from typing import List, Iterator, Union

from core.model.data_source import DataSource
from core.model.project import Project


class SourceDataProvider(ABC):
    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    @abstractmethod
    def test_connection(self) -> bool:
        pass

    @abstractmethod
    def get_identifiers(self) -> List[str]:
        pass

    @abstractmethod
    def get_data(self, identifier: Union[str, None]) -> Iterator:
        pass


class DataSourceUtil:
    EXT_CSV = 'csv'
    EXT_JSON = 'json'
    EXT_SQLITE = ['db', 'sql', 'sqlite', 'sqlite3']

    KIND_CSV = 'CSV'
    KIND_JSON = 'JSON'
    KIND_SQLITE = 'SQLite'
    KIND_POSTGRES = 'PostgreSQL'

    def __init__(self, proj: Project, storage_root: str):
        self._proj = proj
        self._storage_root = storage_root

    @classmethod
    def is_file_allowed(cls, file_name: str) -> bool:
        if '.' not in file_name:
            return False
        ext = cls._extension(file_name)
        return ext in ['csv', 'json']

    @classmethod
    def _extension(cls, file_name: str) -> str:
        return file_name.rsplit('.', 1)[1].lower()

    @classmethod
    def _extension_to_kind(cls, extension: str) -> str:
        if extension == cls.EXT_CSV:
            return cls.KIND_CSV
        elif extension == cls.EXT_JSON:
            return cls.KIND_JSON
        elif extension in cls.EXT_SQLITE:
            return cls.KIND_SQLITE
        raise Exception('unsupported file extension')

    def make_file_path(self, file_name: str):
        return os.path.join(self._storage_root, self._proj.id, file_name)

    def create_file_data_source(self, file_name: str) -> DataSource:
        ext = self._extension(file_name)
        kind = self._extension_to_kind(ext)
        connection_string = None
        if kind == self.KIND_SQLITE:
            file_path = self.make_file_path(file_name)
            connection_string = 'sqlite:///{}'.format(file_path)
        data_source = DataSource(
            kind=kind,
            file_name=file_name,
            connection_string=connection_string,
            project=self._proj
        )
        return data_source

    def create_postgres_data_source(self, user: str, password: str, host: str, database: str) -> DataSource:
        connection_string = 'postgresql://{}:{}@{}/{}'.format(user, password, host, database)
        return DataSource(
            kind=self.KIND_POSTGRES,
            connection_string=connection_string,
            project=self._proj
        )
