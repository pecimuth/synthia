from itertools import zip_longest

from flask.testing import FlaskClient
from sqlalchemy import MetaData, Table, Column, CheckConstraint, PrimaryKeyConstraint, ForeignKeyConstraint, \
    UniqueConstraint, Constraint

from core.service.mock_schema import mock_book_author_publisher
from core.service.types import get_column_type
from tests.fixtures.data_source import UserMockDatabase
from tests.fixtures.project import UserProject
from web.view.data_source import DataSourceView
from web.view.project import ProjectView


def validate_project_view(project_view: dict, meta: MetaData):
    assert not ProjectView().validate(project_view)
    table_set = set()
    for table_view in project_view['tables']:
        name = table_view['name']
        table_set.add(name)
        validate_table(table_view, meta.tables.get(name))
    assert table_set == meta.tables.keys()


def validate_table(table_view: dict, table: Table):
    column_set = set()
    for column_view in table_view['columns']:
        name = column_view['name']
        column: Column = getattr(table.columns, name)
        assert column_view['nullable'] == column.nullable
        assert column_view['col_type'] == get_column_type(column)
        column_set.add(name)
    assert column_set == set(map(lambda c: c.name, table.columns))
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
            assert constraint.name in constraint_dict
            validate_constraint(constraint_dict[constraint.name], constraint)


def validate_constraint(constraint_view: dict, constraint: Constraint):
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


class TestDataSource:
    def test_create_mock(self, client: FlaskClient, user_project: UserProject, auth_header: dict):
        data = {
            'project_id': user_project.project.id
        }
        response = client.post('/api/data-source-mock-database', data=data, headers=auth_header)
        json = response.get_json()
        assert not DataSourceView().validate(json)

    def test_import_from_mock(self,
                              client: FlaskClient,
                              user_mock_database: UserMockDatabase,
                              auth_header: dict):
        url = '/api/data-source/{}/import'.format(user_mock_database.data_source.id)
        response = client.post(url, headers=auth_header)
        json = response.get_json()
        meta = mock_book_author_publisher()
        validate_project_view(json, meta)
