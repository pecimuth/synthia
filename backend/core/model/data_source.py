from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from . import base


class DataSource(base):
    __tablename__ = 'datasource'
    id = Column(Integer, primary_key=True)

    # for test-based formats and SQLite
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)

    # for all databases
    driver = Column(String, nullable=True)  # 'sqlite' | 'postgresql'
    db = Column(String, nullable=True)

    # for databases except SQLite
    usr = Column(String, nullable=True)
    pwd = Column(String, nullable=True)
    host = Column(String, nullable=True)
    port = Column(Integer, nullable=True)

    project_id = Column(Integer, ForeignKey('project.id', ondelete='CASCADE'))
    project = relationship('Project', back_populates='data_sources')

    __table_args__ = (
        Index('ix_datasource_project', project_id),
    )
