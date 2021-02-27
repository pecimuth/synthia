from inspect import signature
from typing import Type, Optional, Callable

from core.service.column_generator.base import ColumnGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.data_source.data_provider import DataProvider
from core.service.types import class_to_types, AnyBasicType

ParameterMethod = Callable[[ColumnGenerator], AnyBasicType]
EstimatorMethod = Callable[[ColumnGenerator, DataProvider], AnyBasicType]


def add_parameter_property(owner: Type[ColumnGenerator],
                           name: str,
                           default_value_method: ParameterMethod,
                           param_options):
    sig = signature(default_value_method)
    param = ColumnGeneratorParam(
        name=name,
        default_value=default_value_method,
        value_type=class_to_types(sig.return_annotation),
        **param_options
    )
    if owner.param_list is ColumnGenerator.param_list:
        owner.param_list = []
    owner.param_list.append(param)

    prop = ParameterProperty(owner, name)
    setattr(owner, name, prop)


class ParameterProperty:
    def __init__(self, owner: Type[ColumnGenerator], name: str):
        self._owner = owner
        self._name = name

    def __set__(self, instance: ColumnGenerator, value: AnyBasicType):
        instance.params[self._name] = value

    def __get__(self, instance: ColumnGenerator, owner: Type[ColumnGenerator]):
        return instance.params[self._name]


class GeneratorParameterDecorator:
    def __init__(self, default_value_method: ParameterMethod, param_options):
        self._param_options = param_options
        self._default_value_method = default_value_method

    def __set_name__(self, owner: Type[ColumnGenerator], name: str):
        add_parameter_property(owner, name, self._default_value_method, self._param_options)

    def estimator(self, estimator_method: EstimatorMethod):
        return EstimatorDecorator(estimator_method, self._default_value_method, self._param_options)


def parameter(method: Optional[ParameterMethod] = None, **kwargs):
    if method is not None:
        return GeneratorParameterDecorator(method, {})

    def wrapper(_method: ParameterMethod):
        return GeneratorParameterDecorator(_method, kwargs)
    return wrapper


class EstimatorDecorator:
    def __init__(self,
                 method: EstimatorMethod,
                 default_value_method: ParameterMethod,
                 param_options):
        self._estimator_method = method
        self._default_value_method = default_value_method
        self._param_options = param_options

    def __set_name__(self, owner: Type[ColumnGenerator], name: str):
        add_parameter_property(owner, name, self._default_value_method, self._param_options)

        def call_the_estimator(generator: ColumnGenerator, provider: DataProvider):
            result = self._estimator_method(generator, provider)
            if result is not None:
                generator.params[name] = result
        if owner.estimator_list is ColumnGenerator.estimator_list:
            owner.estimator_list = []
        owner.estimator_list.append(call_the_estimator)
