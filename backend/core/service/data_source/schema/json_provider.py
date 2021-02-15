from typing import List

from core.model.meta_table import MetaTable
from core.service.data_source.schema import SchemaProvider


class JsonSchemaProvider(SchemaProvider):
    def read_structure(self) -> List[MetaTable]:
        pass
