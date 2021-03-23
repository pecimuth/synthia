from datetime import timedelta, datetime
from typing import NewType

import jwt
from sqlalchemy.orm import Session

from core.model.user import User

SecretKey = NewType('SecretKey', str)
"""Secret key used as an input to the JWT encoder/decoder.

We create a new type so that it can be used with the dependency injector.
"""


class TokenService:
    """Creation and decoding of JWT tokens."""

    ACCESS_TOKEN_VALIDITY = timedelta(days=7)
    """For how long is the token valid."""

    TOKEN_ALGORITHM = 'HS256'

    def __init__(self, secret_key: SecretKey, db_session: Session):
        self._db_session = db_session
        self._secret_key = secret_key

    def create_token(self, user: User) -> str:
        """Create and return a token for the user."""
        payload = {
            'exp': datetime.utcnow() + self.ACCESS_TOKEN_VALIDITY,
            'iat': datetime.utcnow(),
            'sub': user.id
        }
        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self.TOKEN_ALGORITHM
        )

    def decode_token(self, token: str) -> User:
        """Decode the token, fetch and return the user."""
        payload = jwt.decode(
            token,
            self._secret_key,
            algorithms=[self.TOKEN_ALGORITHM]
        )
        user_id = payload['sub']
        return self._db_session.query(User).\
            filter(User.id == user_id).\
            one()
