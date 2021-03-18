from abc import ABC, abstractmethod
from typing import List, Iterable

from core.model.data_source import DataSource
from core.model.meta_table import MetaTable
from core.service.data_source.identifier import Identifier, structure_to_identifiers
from core.service.injector import Injector


class SchemaProvider(ABC):
    def __init__(self, data_source: DataSource, injector: Injector):
        self._data_source = data_source
        self._injector = injector

    @abstractmethod
    def read_structure(self) -> List[MetaTable]:
        """Read the schema from the data source and deserialize it.

        The columns have no assigned generators and the tables
        are not assigned to a project. The implementation of this method
        should check the validity of table and column identifiers.
        """
        pass

    def get_identifiers(self) -> Iterable[Identifier]:
        """Return the list of all identifiers in a data source."""
        return structure_to_identifiers(self.read_structure())
