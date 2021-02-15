from abc import ABC, abstractmethod
from typing import List

from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.facade import find_recommended_generator


class SchemaProvider(ABC):
    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    @abstractmethod
    def read_structure(self) -> List[MetaTable]:
        pass

    @classmethod
    def _set_recommended_generator(cls, meta_column: MetaColumn):
        generator = find_recommended_generator(meta_column)
        if generator is None:
            return
        meta_column.generator_name = generator.name
