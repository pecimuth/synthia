from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from core.model.user import User
from core.service.exception import SomeError
from core.service.auth.password import PasswordService
from core.service.auth.token import TokenService


class UserFacade:
    """Provide CRUD operations related to User."""

    def __init__(self,
                 db_session: Session,
                 token_service: TokenService):
        self._db_session = db_session
        self._token_service = token_service

    def register(self, email: Optional[str], pwd: Optional[str]) -> User:
        """Register a new user.

        Password is not considered for an anonymous user.
        """
        user = User(email=email)
        if email is not None:
            password_service = PasswordService(user)
            if not password_service.is_valid(pwd):
                raise SomeError('Please choose a different password')
            password_service.set_password(pwd)
        self._db_session.add(user)
        return user

    def login(self, email: str, pwd: str) -> User:
        """Login with an email and password. If the credentials
        are correct, return the user."""
        try:
            user: User = self._db_session.query(User).\
                filter(User.email == email).\
                one()
        except NoResultFound:
            raise SomeError('No user found')

        password_service = PasswordService(user)
        if not password_service.check_password(pwd):
            raise SomeError('Wrong password')

        password_service = PasswordService(user)
        if not password_service.check_password(pwd):
            raise SomeError('Wrong password')
        return user

    def get_token(self, user: User) -> str:
        """Create an auth token for the user."""
        return self._token_service.create_token(user)
