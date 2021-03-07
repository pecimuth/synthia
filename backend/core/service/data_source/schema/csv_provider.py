import csv
from typing import List

from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from core.service.data_source.file_common import strip_file_extensions
from core.service.data_source.identifier import Identifier
from core.service.data_source.schema import SchemaProvider
from core.service.data_source.schema.type_deduction import TypeDeduction
from core.service.types import Types


class CsvSchemaProvider(SchemaProvider):
    def read_structure(self) -> List[MetaTable]:
        with open(self._data_source.file_path) as file:
            reader = csv.DictReader(file)
            type_deduction = TypeDeduction()
            for row in reader:
                type_deduction.next_row(row)
        return [
            self._make_table(type_deduction, self._file_name_to_table_name())
        ]

    def _file_name_to_table_name(self) -> str:
        return strip_file_extensions(self._data_source.file_name)

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

    def _make_table(self, type_deduction: TypeDeduction, table_name: str) -> MetaTable:
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
