from itertools import zip_longest

from sqlalchemy import MetaData, Table, Column, CheckConstraint, PrimaryKeyConstraint, ForeignKeyConstraint, \
    UniqueConstraint, Constraint

from core.service.types import get_column_type
from web.view.project import ProjectView


class ProjectViewMetaValidator:
    def __init__(self, project_view: dict, meta: MetaData, check_constraints: bool = True):
        self._project_view = project_view
        self._meta = meta
        self._check_constraints = check_constraints

    def validate(self):
        assert not ProjectView().validate(self._project_view)
        table_set = set()
        for table_view in self._project_view['tables']:
            name = table_view['name']
            table_set.add(name)
            self._validate_table(table_view, self._meta.tables.get(name))
        assert table_set == self._meta.tables.keys()

    def _validate_table(self, table_view: dict, table: Table):
        column_set = set()
        for column_view in table_view['columns']:
            name = column_view['name']
            column: Column = getattr(table.columns, name)
            assert column_view['nullable'] == column.nullable
            assert column_view['col_type'] == get_column_type(column)
            column_set.add(name)
        assert column_set == set(map(lambda c: c.name, table.columns))
        if not self._check_constraints:
            return
        constraint_dict = dict()
        for constraint_view in table_view['constraints']:
            name = constraint_view['name']
            if name is not None:
                constraint_dict[name] = constraint_view
        for constraint in table.constraints:
            if isinstance(constraint, (CheckConstraint,
                                       PrimaryKeyConstraint,
                                       ForeignKeyConstraint,
                                       UniqueConstraint))\
               and constraint.name is not None:
                print(constraint.name, constraint_dict)
                assert constraint.name in constraint_dict
                self._validate_constraint(constraint_dict[constraint.name], constraint)

    @staticmethod
    def _validate_constraint(constraint_view: dict, constraint: Constraint):
        if hasattr(constraint, 'columns'):
            it = zip_longest(constraint.columns, constraint_view['constrained_columns'])
            for column, column_view in it:
                assert column.name == column_view['name']
        if hasattr(constraint, 'elements'):
            it = zip_longest(constraint.elements, constraint_view['referenced_columns'])
            for foreign_key, column_view in it:
                assert foreign_key.column.name == column_view['name']
        if hasattr(constraint, 'sqltext'):
            assert constraint_view['check_expression'] == str(constraint.sqltext)
