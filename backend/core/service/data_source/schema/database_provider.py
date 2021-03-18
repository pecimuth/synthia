from typing import List, Dict, Optional

from sqlalchemy import Column, Table, MetaData, Constraint, CheckConstraint, UniqueConstraint, PrimaryKeyConstraint, \
    ForeignKeyConstraint
from sqlalchemy.exc import SQLAlchemyError

from core.model.column_constraint import ColumnConstraint
from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.model.reference_constraint import ReferenceConstraint
from core.service.data_source.database_common import DatabaseConnectionManager
from core.service.data_source.identifier import Identifier
from core.service.data_source.schema.base_provider import SchemaProvider
from core.service.exception import DataSourceError, DatabaseNotReadable
from core.service.injector import Injector
from core.service.types import get_column_type


class DatabaseSchemaProvider(SchemaProvider):
    """Read the schema of a database, including integrity constraints."""

    def __init__(self, data_source: DataSource, injector: Injector):
        super().__init__(data_source, injector)
        self._table_list: Optional[List[MetaTable]] = []
        self._column: Dict[str, Dict[str, MetaColumn]] = {}

    def read_structure(self) -> List[MetaTable]:
        connection_manager = self._injector.get(DatabaseConnectionManager)
        engine = connection_manager.get_engine(self._data_source)
        meta = MetaData()
        try:
            meta.reflect(bind=engine)
        except SQLAlchemyError:
            raise DatabaseNotReadable(self._data_source)
        self._column = {}
        self._table_list = [
            self._make_meta_table(tab)
            for tab in meta.tables.values()
        ]
        self._add_meta_constraints(meta)
        return self._table_list

    def _make_meta_column(self, table: Table, column: Column) -> MetaColumn:
        meta_column = MetaColumn(
            name=column.name,
            col_type=get_column_type(column),
            nullable=column.nullable,
            data_source=self._data_source,
            reflected_column_idf=repr(Identifier(table.name, column.name))
        )
        return meta_column

    def _make_meta_table(self, table: Table) -> MetaTable:
        """Construct a MetaTable from an SQLAlchemy table, including columns,
        excluding constraints."""
        meta_table = MetaTable(name=table.name, columns=[])
        self._column[table.name] = {}
        for col in table.c.values():
            meta_column = self._make_meta_column(table, col)
            meta_table.columns.append(meta_column)
            self._column[table.name][col.name] = meta_column
        return meta_table

    def _add_meta_constraints(self, meta: MetaData):
        """Add constraints to each meta table."""
        for meta_table, table in zip(self._table_list, meta.tables.values()):
            for constraint in table.constraints:
                meta_constraint = self._make_meta_constraint(meta_table, constraint)
                meta_table.constraints.append(meta_constraint)

    def _make_meta_constraint(self, meta_table: MetaTable, constraint: Constraint) -> MetaConstraint:
        """Create a MetaConstraint from an SQLAlchemy constraint."""
        meta_constraint = MetaConstraint(
            name=constraint.name,
            table=meta_table
        )
        if hasattr(constraint, 'columns'):
            # these are constrained columns
            column_by_name = self._column[meta_table.name]
            for index, column in enumerate(constraint.columns):
                meta_column = column_by_name[column.name]
                column_constraint = ColumnConstraint(column=meta_column,
                                                     constraint=meta_constraint,
                                                     index=index)
                meta_constraint.column_constraint_pairs.append(column_constraint)
        if isinstance(constraint, CheckConstraint):
            meta_constraint.constraint_type = MetaConstraint.CHECK
            meta_constraint.check_expression = str(constraint.sqltext)
        elif isinstance(constraint, UniqueConstraint):
            meta_constraint.constraint_type = MetaConstraint.UNIQUE
        elif isinstance(constraint, PrimaryKeyConstraint):
            meta_constraint.constraint_type = MetaConstraint.PRIMARY
        elif isinstance(constraint, ForeignKeyConstraint):
            meta_constraint.constraint_type = MetaConstraint.FOREIGN
            # elements are ForeignKey instances, mapping one constrained column
            # to the referenced column
            for index, foreign_key in enumerate(constraint.elements):
                column_by_name = self._column[foreign_key.column.table.name]
                meta_column = column_by_name[foreign_key.column.name]
                ref_constraint = ReferenceConstraint(column=meta_column,
                                                     constraint=meta_constraint,
                                                     index=index)
                meta_constraint.reference_constraint_pairs.append(ref_constraint)
        else:
            raise DataSourceError('Unknown constraint type', self._data_source)
        return meta_constraint
