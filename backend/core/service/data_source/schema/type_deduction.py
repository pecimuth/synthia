from typing import Dict, Optional, Set

from core.service.exception import SomeError
from core.service.types import AnyBasicType, Types, get_value_type

ColumnTypes = Dict[str, Types]


class TypeDeduction:
    """Perform type deduction for tabular data.

    Suppose we have the following sequence of values in a column:
    `None, None, 1, 2, 3`
    The type is definitely an int, but we only know from the third
    element. We also detect inconsistent types:
    `None, 1, 'string'`
    An exception is raised when the third element is processed.
    Sequences without None values are assumed to be NOT NULL.
    """
    Row = Dict[str, AnyBasicType]

    TYPES_NUMERIC = [Types.INTEGER, Types.FLOAT]

    def __init__(self):
        self._types: Optional[ColumnTypes] = None
        self._nullable: Set[str] = set()

    def next_row(self, row: Row):
        """Process another row of data, deduce types
        and check for inconsistencies"""
        column_types = self._deduct_types(row)
        self._update_nullable(row)
        if self._types is None:
            self._types = column_types
        else:
            if not self._is_consistent(column_types):
                raise SomeError('Inconsistent types')
            self._merge_with(column_types)

    def get_types(self) -> ColumnTypes:
        """Return the deduced types. Columns with None values
        are assumed to be string.

        In case there are no rows, return an empty dictionary.
        """
        if self._types is None:
            return {}
        return {
            key: Types.STRING if value == Types.NONE else value
            for key, value in self._types.items()
        }

    def is_nullable(self, col_name: str) -> bool:
        """Return whether the column identified by name is nullable."""
        return col_name in self._nullable

    @classmethod
    def _deduct_types(cls, row: Row) -> ColumnTypes:
        """Deduce column types from a row of values.

        Whole numbers (floats) are converted to ints.
        """
        return {
            key: get_value_type(cls.whole_number_to_int(value))
            for key, value in row.items()
        }

    @staticmethod
    def whole_number_to_int(value: AnyBasicType) -> AnyBasicType:
        """Convert the value to int in case it is a whole number of type float.
        Return the original value otherwise."""
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value

    def _is_consistent(self, types: ColumnTypes) -> bool:
        for key, value_type in types.items():
            if key not in self._types:
                raise SomeError('Unexpected column {}'.format(key))
            saved_type = self._types[key]
            if saved_type == Types.NONE:
                continue
            if value_type != Types.NONE and value_type != saved_type:
                # float/integer is consistent - values are converted to float
                return value_type in self.TYPES_NUMERIC and saved_type in self.TYPES_NUMERIC
        return True

    def _merge_with(self, types: ColumnTypes):
        for key, value_type in types.items():
            saved_type = self._types[key]
            # everything overrides None, float overrides int
            if saved_type == Types.NONE or value_type == Types.FLOAT:
                self._types[key] = value_type

    def _update_nullable(self, row: Row):
        for key, value in row.items():
            if value is None:
                self._nullable.add(key)
