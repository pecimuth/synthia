from typing import Any, List

from sqlalchemy import MetaData, Table, Column, ForeignKeyConstraint, PrimaryKeyConstraint, UniqueConstraint, \
    CheckConstraint, Constraint

from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.data_source.identifier import Identifier
from core.service.exception import SomeError
from core.service.types import get_sql_alchemy_type


class StructureDeserializer:
    """Convert meta entities into SQL Alchemy entities."""

    def __init__(self, proj: Project):
        self._proj = proj

    @classmethod
    def _deserialize_table(cls, meta_table: MetaTable, meta: MetaData) -> Table:
        """Convert meta table into SQL Alchemy table."""
        columns = [cls._deserialize_column(col) for col in meta_table.columns]
        constraints = cls._make_constraints(meta_table)
        table = Table(
            meta_table.name,
            meta,
            *columns,
            *constraints
        )
        return table

    @classmethod
    def _deserialize_column(cls, meta_column: MetaColumn) -> Column:
        """Convert meta column into SQL Alchemy column."""
        column = Column(
            meta_column.name,
            get_sql_alchemy_type(meta_column.col_type),
            nullable=meta_column.nullable
        )
        return column

    @classmethod
    def _make_constraints(cls, meta_table: MetaTable) -> List[Constraint]:
        """Convert meta constraints into SQL Alchemy constraints."""
        constraints = []
        for meta_constraint in meta_table.constraints:
            constrained_columns: Any = [
                meta_column.name
                for meta_column in meta_constraint.constrained_columns
            ]
            if meta_constraint.constraint_type == MetaConstraint.FOREIGN:
                referenced_columns = [
                    repr(Identifier(meta_column.table.name, meta_column.name))
                    for meta_column in meta_constraint.referenced_columns
                ]
                constraint = ForeignKeyConstraint(
                    constrained_columns,
                    referenced_columns,
                    name=meta_constraint.name
                )
            elif meta_constraint.constraint_type == MetaConstraint.PRIMARY:
                constraint = PrimaryKeyConstraint(
                    *constrained_columns,
                    name=meta_constraint.name
                )
            elif meta_constraint.constraint_type == MetaConstraint.UNIQUE:
                constraint = UniqueConstraint(
                    *constrained_columns,
                    name=meta_constraint.name
                )
            elif meta_constraint.constraint_type == MetaConstraint.CHECK:
                constraint = CheckConstraint(meta_constraint.check_expression)
            else:
                raise SomeError('Unknown constraint type')
            constraints.append(constraint)
        return constraints

    def deserialize(self) -> MetaData:
        """Convert all project entities into SQL Alchemy Meta Data."""
        meta = MetaData()
        for table in self._proj.tables:
            self._deserialize_table(table, meta)
        return meta
