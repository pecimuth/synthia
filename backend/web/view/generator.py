from marshmallow import Schema, ValidationError
from marshmallow.fields import Integer, Str, Dict, Float, Bool, Raw, Nested, List, Method
from marshmallow.validate import Range

from core.service.column_generator import get_generator_by_name
from core.service.exception import SomeError


class GeneratorSettingView(Schema):
    id = Integer()
    name = Str()
    params = Dict(keys=Str())
    null_frequency = Float()


def validate_generator_name(name):
    try:
        get_generator_by_name(name)
    except SomeError as e:
        raise ValidationError(e.message)


class GeneratorSettingWrite(Schema):
    name = Str(validate=validate_generator_name, required=False)
    params = Dict(keys=Str(), required=False)
    null_frequency = Float(validate=Range(min=0, max=1), required=False)
    estimate_params = Bool(required=False)


class GeneratorSettingCreate(Schema):
    table_id = Integer()
    name = Str(validate=validate_generator_name)
    params = Dict(keys=Str())
    null_frequency = Float(validate=Range(min=0, max=1))
    column_id = Integer(required=False)


class GeneratorParam(Schema):
    name = Str()
    value_type = Str()

    min_value = Raw()
    max_value = Raw()
    greater_equal_than = Str(allow_none=True)


class GeneratorView(Schema):
    name = Str()
    category = Method('get_category_value')
    only_for_type = Str()
    supports_null = Bool()
    param_list = List(Nested(GeneratorParam()))

    def get_category_value(self, obj):
        return obj.category.value


class GeneratorListView(Schema):
    items = List(Nested(GeneratorView()))
