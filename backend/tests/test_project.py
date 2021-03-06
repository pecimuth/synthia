from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from core.model.project import Project
from tests.fixtures.project import UserProject
from web.view.project import ProjectView, ProjectListView, PreviewView


class TestProject:

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
        url = '/api/project/{}/preview'.format(user_project.project.id)
        data = {
            'rows': []
        }
        response = client.post(url, json=data, headers=auth_header)
        json = response.get_json()
        assert not PreviewView().validate(json)
