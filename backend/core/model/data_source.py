from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import base


class DataSource(base):
    __tablename__ = 'datasource'
    id = Column(Integer, primary_key=True)
    kind = Column(String) # CSV, CSV-Metadata, JSON, XML, SQLite, PostgreSQL

    # for test-based formats and SQLite
    file_name = Column(String, nullable=True)

    # for databases incl. SQLite
    connection_string = Column(String, nullable=True)

    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship('Project', back_populates='data_sources')
