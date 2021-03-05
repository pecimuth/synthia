from inspect import signature
from itertools import islice
from typing import TypeVar, Type


class Injector:
    T = TypeVar('T')

    def __init__(self):
        self._instances: dict = {}

    def get(self, typ: Type[T]) -> T:
        if typ in self._instances:
            return self._instances[typ]
        constructed = self._construct(typ)
        self._instances[typ] = constructed
        return constructed

    def provide(self, typ: Type[T], inst: T):
        self._instances[typ] = inst

    def _construct(self, typ: Type[T]) -> T:
        sig = signature(typ.__init__)
        dependencies = []
        for param in islice(sig.parameters.values(), 1, None):
            inst = self.get(param.annotation)
            dependencies.append(inst)
        return typ(*dependencies)
