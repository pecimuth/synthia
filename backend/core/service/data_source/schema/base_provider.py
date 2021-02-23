from abc import ABC, abstractmethod
from typing import List, Iterable

from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.column_generator import make_generator_instance_for_meta_column
from core.service.data_source.identifier import Identifier, structure_to_identifiers
from core.service.exception import SomeError


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
        try:
            generator_instance = make_generator_instance_for_meta_column(meta_column)
            generator_instance.estimate_params()
        except SomeError:
            pass

    @classmethod
    def _set_recommended_generators_for_list(cls, table_list: List[MetaTable]):
        for table in table_list:
            for column in table.columns:
                cls._set_recommended_generator(column)
