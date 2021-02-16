from abc import ABC, abstractmethod
from typing import List, Iterable

from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator.facade import find_recommended_generator
from core.service.data_source.identifier import Identifier, structure_to_identifiers


class SchemaProvider(ABC):
    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    @abstractmethod
    def read_structure(self) -> List[MetaTable]:
        pass

    def get_identifiers(self) -> Iterable[Identifier]:
        return structure_to_identifiers(self.read_structure())

    @classmethod
    def _set_recommended_generator(cls, meta_column: MetaColumn):
        generator_factory = find_recommended_generator(meta_column)
        if generator_factory is None:
            return
        meta_column.generator_name = generator_factory.name
        generator = generator_factory(meta_column)
        generator.estimate_params()
        # TODO
        meta_column.generator_params = generator._params
