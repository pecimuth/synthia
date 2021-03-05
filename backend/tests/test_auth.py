from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from core.model.user import User
from core.service.auth.token import TokenService
from core.service.injector import Injector
from tests.fixtures.user import USER_PASSWORD


class TestAuth:
    def test_anon_register(self, client: FlaskClient, session: Session, injector: Injector):
        result = client.post('/api/auth/register')
        json = result.get_json()
        user = session.query(User).filter(User.id == json['user']['id']).one()
        token_service = injector.get(TokenService)
        token_user = token_service.decode_token(json['token'])
        assert user is token_user

    def test_login(self, client: FlaskClient, user: User, injector: Injector):
        data = {
            'email': user.email,
            'pwd': USER_PASSWORD
        }
        result = client.post('/api/auth/login', data=data)
        json = result.get_json()
        assert json['user']['id'] == user.id
        token_service = injector.get(TokenService)
        token_user = token_service.decode_token(json['token'])
        assert user is token_user

    def test_wrong_password(self, client: FlaskClient, user: User):
        data = {
            'email': user.email,
            'pwd': 'not the password'
        }
        result = client.post('/api/auth/login', data=data)
        assert result.status_code == 400

    def test_user(self, client: FlaskClient, user: User, auth_header: dict):
        result = client.get('/api/auth/user', headers=auth_header)
        json = result.get_json()
        assert json['id'] == user.id

    def test_not_authenticated(self, client: FlaskClient):
        result = client.get('/api/auth/user')
        assert result.status_code == 400
        result = client.get('/api/auth/user', headers={'Authorization': 'Bearer made.up.token'})
        assert result.status_code == 400
