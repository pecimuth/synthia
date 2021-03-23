import pytest

from core.facade.user import UserFacade
from core.model.user import User
from core.service.auth.token import TokenService

USER_PASSWORD = 'bar'


@pytest.fixture
def user(injector, session) -> User:
    """Register a user."""
    facade = injector.get(UserFacade)
    user = facade.register('foo', USER_PASSWORD)
    session.commit()
    injector.provide(User, user)
    yield user
    if session.is_active:
        session.delete(user)


@pytest.fixture
def auth_header(user, injector) -> dict:
    """Create an auth header with JWT token for the user."""
    token_service = injector.get(TokenService)
    token = token_service.create_token(user)
    return {
        'Authorization': 'Bearer {}'.format(token)
    }
