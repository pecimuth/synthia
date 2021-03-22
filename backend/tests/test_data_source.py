from io import BytesIO
from typing import Tuple

from flask.testing import FlaskClient
from sqlalchemy import MetaData

from core.service.mock_schema import mock_book_author_publisher
from tests.fixtures.data_source import UserMockDataSource
from tests.fixtures.project import UserProject
from tests.validator.project_view_meta import ProjectViewMetaValidator
from web.view.data_source import DataSourceView


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
                              user_mock_database: UserMockDataSource,
                              auth_header: dict):
        url = '/api/data-source/{}/import'.format(user_mock_database.data_source.id)
        response = client.post(url, headers=auth_header)
        json = response.get_json()
        meta = mock_book_author_publisher()
        validator = ProjectViewMetaValidator(json, meta)
        validator.validate()

    def test_upload_json(self,
                         client: FlaskClient,
                         user_project: UserProject,
                         mock_json_file: Tuple[BytesIO, str],
                         auth_header: dict):
        data = {
            'project_id': str(user_project.project.id),
            'data_file': mock_json_file
        }
        response = client.post(
            '/api/data-source-file',
            data=data,
            headers=auth_header,
            content_type='multipart/form-data'
        )
        json = response.get_json()
        assert not DataSourceView().validate(json)

    def test_import_from_json(self,
                              client: FlaskClient,
                              user_mock_json: UserMockDataSource,
                              mock_json_meta: MetaData,
                              auth_header: dict):
        url = '/api/data-source/{}/import'.format(user_mock_json.data_source.id)
        response = client.post(url, headers=auth_header)
        json = response.get_json()
        validator = ProjectViewMetaValidator(json, mock_json_meta, False)
        validator.validate()

    def test_import_from_csv(self,
                             client: FlaskClient,
                             user_mock_csv: UserMockDataSource,
                             mock_csv_meta: MetaData,
                             auth_header: dict):
        url = '/api/data-source/{}/import'.format(user_mock_csv.data_source.id)
        response = client.post(url, headers=auth_header)
        json = response.get_json()
        validator = ProjectViewMetaValidator(json, mock_csv_meta, False)
        validator.validate()

    def test_import_from_circular(self,
                                  client: FlaskClient,
                                  user_mock_circular_database: UserMockDataSource,
                                  circular_meta: MetaData,
                                  auth_header: dict):
        url = '/api/data-source/{}/import'.format(user_mock_circular_database.data_source.id)
        response = client.post(url, headers=auth_header)
        json = response.get_json()
        validator = ProjectViewMetaValidator(json, circular_meta)
        validator.validate()
