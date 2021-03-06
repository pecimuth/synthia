from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.engine.url import URL

from core.model.data_source import DataSource


class DatabaseConnectionManager:
    def __init__(self):
        self._engine: Dict[int, Engine] = {}
        self._connection: Dict[int, Connection] = {}

    @classmethod
    def create_database_source_engine(cls, data_source: DataSource) -> Engine:
        url = URL(
            drivername=data_source.driver,
            username=data_source.usr,
            password=data_source.pwd,
            host=data_source.host,
            port=data_source.port,
            database=data_source.db
        )
        return create_engine(url)

    def get_engine(self, data_source: DataSource) -> Engine:
        if data_source.id in self._engine:
            return self._engine[data_source.id]
        engine = self.create_database_source_engine(data_source)
        self._engine[data_source.id] = engine
        return engine

    def get_connection(self, data_source: DataSource):
        if data_source.id in self._connection:
            return self._connection[data_source.id]
        conn = self.get_engine(data_source).connect()
        self._connection[data_source.id] = conn
        return conn

    def clean_up(self):
        while self._connection:
            _, conn = self._connection.popitem()
            conn.close()
        self._engine.clear()
