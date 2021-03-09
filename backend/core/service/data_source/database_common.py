from typing import Dict, Union

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError

from core.model.data_source import DataSource
from core.service.exception import DatabaseConnectionError
from core.service.injector import HasCleanUp

DataSourceOrUrl = Union[DataSource, str]


class DatabaseConnectionManager(HasCleanUp):
    def __init__(self):
        self._engine: Dict[DataSourceOrUrl, Engine] = {}
        self._connection: Dict[DataSourceOrUrl, Connection] = {}

    @classmethod
    def create_database_source_engine(cls, data_source_url: DataSourceOrUrl) -> Engine:
        if isinstance(data_source_url, DataSource):
            data_source = data_source_url
            url = URL(
                drivername=data_source.driver,
                username=data_source.usr,
                password=data_source.pwd,
                host=data_source.host,
                port=data_source.port,
                database=data_source.db
            )
        else:
            url = data_source_url
        return create_engine(url)

    def get_engine(self, data_source_url: DataSourceOrUrl) -> Engine:
        if data_source_url in self._engine:
            return self._engine[data_source_url]
        engine = self.create_database_source_engine(data_source_url)
        self._engine[data_source_url] = engine
        return engine

    def get_connection(self, data_source_url: DataSourceOrUrl):
        if data_source_url in self._connection:
            return self._connection[data_source_url]
        try:
            conn = self.get_engine(data_source_url).connect()
        except SQLAlchemyError:
            raise DatabaseConnectionError()
        self._connection[data_source_url] = conn
        return conn

    def clean_up(self):
        while self._connection:
            _, conn = self._connection.popitem()
            conn.close()
        self._engine.clear()
