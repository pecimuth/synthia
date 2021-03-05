import pytest

from core.facade.user import UserFacade
from core.model.user import User
from core.service.auth.token import TokenService

USER_PASSWORD = 'bar'


@pytest.fixture
def user(injector, session) -> User:
    facade = injector.get(UserFacade)
    user = facade.register('foo', USER_PASSWORD)
    session.commit()
    yield user
    session.delete(user)
    session.commit()


@pytest.fixture
def auth_header(user, injector) -> dict:
    token_service = injector.get(TokenService)
    token = token_service.create_token(user)
    return {
        'Authorization': 'Bearer {}'.format(token)
    }

