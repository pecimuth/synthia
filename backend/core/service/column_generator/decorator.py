from inspect import signature
from typing import Type, Optional, Callable

from core.service.column_generator.base import ColumnGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.data_source.data_provider import DataProvider
from core.service.types import class_to_types, AnyBasicType

ParameterMethod = Callable[[ColumnGenerator], AnyBasicType]
EstimatorMethod = Callable[[ColumnGenerator, DataProvider], AnyBasicType]


class ParameterProperty:
    def __init__(self, param_name: str, owner: Type[ColumnGenerator]):
        self._owner = owner
        self._param_name = param_name

    def __set__(self, instance: ColumnGenerator, value: AnyBasicType):
        instance.params[self._param_name] = value

    def __get__(self, instance: ColumnGenerator, owner: Type[ColumnGenerator]):
        return instance.params[self._param_name]


class GeneratorParameterDecorator:
    def __init__(self, method: ParameterMethod, **kwargs):
        self._kwargs = kwargs
        self._method = method

    def __set_name__(self, owner: Type[ColumnGenerator], name: str):
        sig = signature(self._method)
        param = ColumnGeneratorParam(
            name=name,
            default_value=self._method,
            value_type=class_to_types(sig.return_annotation),
            **self._kwargs
        )
        if owner.param_list is ColumnGenerator.param_list:
            owner.param_list = []
        owner.param_list.append(param)
        prop = ParameterProperty(name, owner)
        setattr(owner, name, prop)


def parameter(method: Optional[ParameterMethod] = None, **kwargs):
    if method is not None:
        return GeneratorParameterDecorator(method)

    def wrapper(_method: ParameterMethod):
        return GeneratorParameterDecorator(_method, **kwargs)
    return wrapper


class EstimatorDecorator:
    def __init__(self, method: EstimatorMethod, param_name: str):
        self._method = method
        self._param_name = param_name

    def __set_name__(self, owner: Type[ColumnGenerator], name: str):
        def call_the_estimator(generator: ColumnGenerator, provider: DataProvider):
            result = self._method(generator, provider)
            if result is not None:
                generator.params[self._param_name] = result
        if owner.estimator_list is ColumnGenerator.estimator_list:
            owner.estimator_list = []
        owner.estimator_list.append(call_the_estimator)


def estimate(param_name: str):
    def wrapper(method: EstimatorMethod):
        return EstimatorDecorator(method, param_name)
    return wrapper
