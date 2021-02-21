from datetime import timedelta, datetime
from typing import Union

import jwt

from core.model.user import User
from web.service.database import get_db_session


class TokenService:
    ACCESS_TOKEN_VALIDITY = timedelta(days=7)
    TOKEN_ALGORITHM = 'HS256'

    def __init__(self, secret_key: str, user: Union[User, None] = None):
        self._user = user
        self._secret_key = secret_key

    def create_token(self) -> str:
        assert self._user is not None
        payload = {
            'exp': datetime.utcnow() + self.ACCESS_TOKEN_VALIDITY,
            'iat': datetime.utcnow(),
            'sub': self._user.id
        }
        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self.TOKEN_ALGORITHM
        )

    def decode_token(self, token: str) -> User:
        payload = jwt.decode(
            token,
            self._secret_key,
            algorithms=[self.TOKEN_ALGORITHM]
        )
        user_id = payload['sub']
        self._user = get_db_session().query(User).filter(User.id == user_id).one()
        return self._user
