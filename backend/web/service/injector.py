from typing import TypeVar, Type

from flask import g, current_app
from sqlalchemy.orm import Session

from core.facade.project import ProjectStorage
from core.service.auth.token import SecretKey
from core.service.injector import Injector
from web.service.database import get_db_session


def get_injector() -> Injector:
    if 'injector' in g:
        return g.injector
    injector = Injector()
    injector.provide(Session, get_db_session())
    injector.provide(SecretKey, current_app.config['SECRET_KEY'])
    injector.provide(ProjectStorage, current_app.config['PROJECT_STORAGE'])
    g.injector = injector
    return injector


T = TypeVar('T')


def inject(typ: Type[T]) -> T:
    return get_injector().get(typ)


def pop_injector(e=None):
    injector = g.pop('injector', None)
    if injector is not None:
        injector.clean_up()
