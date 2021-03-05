from typing import TypeVar, Type

from flask import g, current_app
from sqlalchemy.orm import Session

from core.service.auth.token import SecretKey
from core.service.injector import Injector
from web.service.database import get_db_session


def get_injector() -> Injector:
    if 'injector' in g:
        return g.injector
    injector = Injector()
    injector.provide(Session, get_db_session())
    injector.provide(SecretKey, current_app.config['SECRET_KEY'])
    g.injector = injector
    return injector


T = TypeVar('T')


def inject(typ: Type[T]) -> T:
    return get_injector().get(typ)


def pop_injector(e=None):
    g.pop('injector', None)
