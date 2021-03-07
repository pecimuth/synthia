from typing import Dict, Optional, Set

from core.service.exception import SomeError
from core.service.types import AnyBasicType, Types, get_value_type

ColumnTypes = Dict[str, Types]


class TypeDeduction:
    Row = Dict[str, AnyBasicType]

    def __init__(self):
        self._types: Optional[ColumnTypes] = None
        self._nullable: Set[str] = set()

    def next_row(self, row: Row):
        column_types = self._deduct_types(row)
        self._update_nullable(row)
        if self._types is None:
            self._types = column_types
        else:
            if not self._is_consistent(column_types):
                raise SomeError('Inconsistent types')
            self._merge_with(column_types)

    def get_types(self) -> ColumnTypes:
        return {
            key: Types.STRING if value == Types.NONE else value
            for key, value in self._types.items()
        }

    def is_nullable(self, col_name: str) -> bool:
        return col_name in self._nullable

    @staticmethod
    def _deduct_types(row: Row) -> ColumnTypes:
        return {
            key: get_value_type(value)
            for key, value in row.items()
        }

    def _is_consistent(self, types: ColumnTypes) -> bool:
        for key, value_type in types.items():
            if key not in self._types:
                raise SomeError('Unexpected column {}'.format(key))
            saved_type = self._types[key]
            if saved_type == Types.NONE:
                continue
            if value_type != Types.NONE and value_type != saved_type:
                return False
        return True

    def _merge_with(self, types: ColumnTypes):
        for key, value_type in types.items():
            saved_type = self._types[key]
            if saved_type == Types.NONE:
                self._types[key] = value_type

    def _update_nullable(self, row: Row):
        for key, value in row.items():
            if value is None:
                self._nullable.add(key)
