import json
from typing import List, Dict, Any

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.file_common import strip_file_extensions
from core.service.data_source.identifier import Identifier
from core.service.data_source.schema import SchemaProvider
from core.service.types import get_value_type

JsonRow = Dict[str, Any]
JsonTable = List[JsonRow]
JsonTableDict = Dict[str, JsonTable]
JsonTableType = Dict[str, str]


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
        raise Exception('invalid format')

    def _file_name_to_table_name(self) -> str:
        return strip_file_extensions(self._data_source.file_name)

    @classmethod
    def _is_json_table(cls, obj) -> bool:
        if not isinstance(obj, list):
            return False
        table_type = None
        for row in obj:
            row_type = cls._row_to_type(row)
            if table_type is None:
                table_type = row_type
            elif not cls._is_consistent(table_type, row_type):
                return False
        return True

    @classmethod
    def _row_to_type(cls, row: JsonRow) -> JsonTableType:
        return {
            column: get_value_type(value)
            for column, value in row.items()
        }

    def _type_to_column(self, table_name: str, col_name: str, type_literal: str) -> MetaColumn:
        return MetaColumn(
            name=col_name,
            col_type=type_literal,
            nullable=False,
            primary_key=False,
            data_source=self._data_source,
            reflected_column_idf=repr(Identifier(table_name, col_name))
        )

    @classmethod
    def _is_consistent(cls, lhs: JsonTableType, rhs: JsonTableType) -> bool:
        return lhs.keys() == rhs.keys()  # TODO check types

    @classmethod
    def _is_json_table_dict(cls, obj) -> bool:
        if not isinstance(obj, dict):
            return False
        return all(map(cls._is_json_table, obj.values()))

    def _parse_table(self, obj: JsonTable, table_name: str) -> MetaTable:
        table_type = {}
        if len(obj) > 0:
            table_type = self._row_to_type(obj[0])
        return MetaTable(
            name=table_name,
            data_source=self._data_source,
            columns=[
                self._type_to_column(table_name, col_name, type_name)
                for col_name, type_name in table_type.items()
            ]
        )

    def _parse_table_dict(self, obj: JsonTableDict) -> List[MetaTable]:
        return [
            self._parse_table(table_content, table_name)
            for table_name, table_content in obj.items()
        ]
