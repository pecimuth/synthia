import json
from typing import List, Dict, Any

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.file_common import strip_file_extensions
from core.service.data_source.identifier import Identifier
from core.service.data_source.schema import SchemaProvider
from core.service.data_source.schema.type_deduction import TypeDeduction
from core.service.exception import DataSourceError
from core.service.types import Types, AnyBasicType

JsonRow = Dict[str, AnyBasicType]
JsonTable = List[JsonRow]
JsonTableDict = Dict[str, JsonTable]


class JsonSchemaProvider(SchemaProvider):
    def read_structure(self) -> List[MetaTable]:
        with open(self._data_source.file_path) as file:
            obj = json.loads(file.read())
            if self._is_json_table_dict(obj):
                return self._parse_table_dict(obj)
            elif self._is_json_table(obj):
                return [
                    self._parse_table(
                        obj,
                        self._file_name_to_table_name()
                    )
                ]
        raise DataSourceError('Invalid JSON structure', self._data_source)

    def _file_name_to_table_name(self) -> str:
        return strip_file_extensions(self._data_source.file_name)

    @classmethod
    def _is_json_row(cls, row) -> bool:
        if isinstance(row, dict):
            return False
        for key, val in row.items():
            if not isinstance(val, (str, int, float, type(None))):
                return False
        return True

    @classmethod
    def _is_json_table(cls, obj) -> bool:
        if not isinstance(obj, list):
            return False
        for row in obj:
            cls._is_json_row(row)
        return True

    @classmethod
    def _is_json_table_dict(cls, obj) -> bool:
        if not isinstance(obj, dict):
            return False
        return all(map(cls._is_json_table, obj.values()))

    def _make_column(self,
                     table_name: str,
                     col_name: str,
                     type_name: Types,
                     nullable: bool) -> MetaColumn:
        return MetaColumn(
            name=col_name,
            col_type=type_name,
            nullable=nullable,
            data_source=self._data_source,
            reflected_column_idf=repr(Identifier(table_name, col_name))
        )

    def _parse_table(self, obj: JsonTable, table_name: str) -> MetaTable:
        type_deduction = TypeDeduction()
        for row in obj:
            type_deduction.next_row(row)
        return MetaTable(
            name=table_name,
            data_source=self._data_source,
            columns=[
                self._make_column(table_name,
                                  col_name,
                                  type_name,
                                  type_deduction.is_nullable(col_name))
                for col_name, type_name in type_deduction.get_types().items()
            ]
        )

    def _parse_table_dict(self, obj: JsonTableDict) -> List[MetaTable]:
        return [
            self._parse_table(table_content, table_name)
            for table_name, table_content in obj.items()
        ]
