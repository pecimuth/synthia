from abc import ABC, abstractmethod
from inspect import signature
from itertools import islice
from typing import TypeVar, Type


class HasCleanUp(ABC):
    """Interface for injectable objects with a clean up routine."""

    @abstractmethod
    def clean_up(self):
        """The clean up routine.

        Will be called once at the end of lifetime.
        """
        pass


class Injector:
    """Provide singleton instances of services
    based on constructor type annotations."""

    T = TypeVar('T')

    def __init__(self):
        self._instances: dict = {}
        self.provide(Injector, self)

    def get(self, typ: Type[T]) -> T:
        """Return a shared instance of a type.

        If an instance of the type is already created, it will be returned.
        If it does not exist yet, it will be recursively constructed.
        """
        if typ in self._instances:
            return self._instances[typ]
        constructed = self._construct(typ)
        self._instances[typ] = constructed
        return constructed

    def provide(self, typ: Type[T], inst: T):
        """Set an instance for a type."""
        self._instances[typ] = inst

    def _construct(self, typ: Type[T]) -> T:
        """Recursively construct and return an instance of a type,
        injecting dependencies for constructors based on type annotations.
        """
        sig = signature(typ.__init__)
        dependencies = []
        for param in islice(sig.parameters.values(), 1, None):
            inst = self.get(param.annotation)
            dependencies.append(inst)
        return typ(*dependencies)

    def __contains__(self, item: Type[T]) -> bool:
        """Return whether an instance for a type is created."""
        return item in self._instances

    def clean_up(self):
        """Forget all instances and call their clean up routines."""
        while self._instances:
            typ, inst = self._instances.popitem()
            if isinstance(inst, HasCleanUp):
                inst.clean_up()
