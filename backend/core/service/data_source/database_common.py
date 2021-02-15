from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL

from core.model.data_source import DataSource


def create_database_source_engine(data_source: DataSource) -> Engine:
    url = URL(
        drivername=data_source.driver,
        username=data_source.usr,
        password=data_source.pwd,
        host=data_source.host,
        port=data_source.port,
        database=data_source.db
    )
    return create_engine(url)
