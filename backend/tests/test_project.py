from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from core.model.project import Project
from web.view.project import ProjectView, ProjectListView


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
