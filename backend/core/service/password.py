import os
from hashlib import scrypt
from typing import Tuple

from core.model.user import User


class PasswordService:
    COST_FACTOR = 1 << 14
    BLOCK_SIZE = 8
    PARALLELIZATION_FACTOR = 1
    SALT_BYTES = 32
    STR_ENCODING = 'utf-8'
    MAX_LENGTH = 256

    def __init__(self, user: User):
        self._user: User = user

    def set_password(self, plain_password: str):
        hashed, salt = self._generate_hash_salt(plain_password)
        self._user.pwd = hashed
        self._user.salt = salt

    def check_password(self, plain_password: str) -> bool:
        return self.is_valid(plain_password) and \
            self._check_match(
                plain_password,
                self._user.pwd,
                self._user.salt
            )

    @classmethod
    def is_valid(cls, plain_password: str) -> bool:
        return isinstance(plain_password, str) and \
               len(plain_password) <= cls.MAX_LENGTH

    @classmethod
    def _generate_hash_salt(cls, input_password: str) -> Tuple[bytes, bytes]:
        salt = os.urandom(cls.SALT_BYTES)
        hashed = cls._call_scrypt(input_password, salt)
        return hashed, salt

    @classmethod
    def _check_match(cls, input_password: str, hashed_password: bytes, salt: bytes) -> bool:
        input_hashed = cls._call_scrypt(input_password, salt)
        return input_hashed == hashed_password

    @classmethod
    def _call_scrypt(cls, plain_password: str, salt: bytes) -> bytes:
        return scrypt(
            plain_password.encode(cls.STR_ENCODING),
            salt=salt,
            n=cls.COST_FACTOR,
            r=cls.BLOCK_SIZE,
            p=cls.PARALLELIZATION_FACTOR
        )
