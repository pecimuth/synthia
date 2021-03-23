from flask.testing import FlaskClient
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

from core.model.project import Project
from core.service.generation_procedure.requisition import ExportRequisitionRow
from tests.fixtures.data_source import UserMockDataSource
from tests.fixtures.project import UserProject
from web.view.project import ProjectView, ProjectListView, PreviewView, ExportRequisitionRowView


class TestProject:
    """Tests related to the project endpoints."""

    def test_projects(self, client: FlaskClient, auth_header: dict):
        response = client.get('/api/projects', headers=auth_header)
        json = response.get_json()
        assert not ProjectListView().validate(json)
        assert len(json['items']) == 0

    def test_create(self, client: FlaskClient, session: Session, auth_header: dict):
        data = {
            'name': 'Foo Bar'
        }
        response = client.post('/api/project', data=data, headers=auth_header)
        json = response.get_json()
        assert not ProjectView().validate(json)
        assert json['name'] == data['name']
        project = session.query(Project).filter(Project.id == json['id']).one()
        assert project.name == data['name']

    def test_get(self, client: FlaskClient, user_project: UserProject, auth_header: dict):
        response = client.get('/api/project/{}'.format(user_project.project.id), headers=auth_header)
        json = response.get_json()
        assert not ProjectView().validate(json)
        assert json['id'] == user_project.project.id

    def test_not_found(self, client: FlaskClient, auth_header: dict):
        response = client.get('/api/project/0', headers=auth_header)
        assert response.status_code == 400

    def test_preview(self, client: FlaskClient, user_project: UserProject, auth_header: dict):
        """Test the preview endpoint with an empty requisition."""
        url = '/api/project/{}/preview'.format(user_project.project.id)
        data = {
            'rows': []
        }
        response = client.post(url, json=data, headers=auth_header)
        json = response.get_json()
        assert not PreviewView().validate(json)

    def test_preview_circular(self,
                              client: FlaskClient,
                              user_import_circular_database: UserMockDataSource,
                              circular_meta: MetaData,
                              auth_header: dict):
        """Test data generation for circular dependencies."""
        # create the preview
        row_count = 10
        url = '/api/project/{}/preview'.format(user_import_circular_database.project.id)

        def make_requisition_row(table: Table):
            row = ExportRequisitionRow(table_name=table.name, row_count=row_count, seed=42)
            return ExportRequisitionRowView().dump(row)
        data = {
            'rows': list(map(make_requisition_row, circular_meta.tables.values()))
        }
        response = client.post(url, json=data, headers=auth_header)
        json = response.get_json()
        assert not PreviewView().validate(json)

        for table_name in circular_meta.tables.keys():
            rows = json['tables'][table_name]
            assert len(rows) == row_count
            # assert that not all FKs in a table are None
            is_fk_none = map(lambda row: row['fid'] is None, rows)
            assert not all(is_fk_none)
