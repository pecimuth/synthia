from marshmallow import Schema, post_load
from marshmallow.fields import Integer, Str, Bool, Nested
from marshmallow.validate import Regexp

from core.model.meta_column import MetaColumn
from core.service.data_source.identifier import Identifier
from web.view.generator import GeneratorSettingView


class ColumnBriefView(Schema):
    id = Integer()
    name = Str()


class ColumnTableBriefView(Schema):
    id = Integer()
    table_id = Integer()
    name = Str()


class ColumnView(Schema):
    id = Integer()
    name = Str()
    col_type = Str()
    nullable = Bool()
    generator_setting = Nested(GeneratorSettingView())

    @post_load
    def make_meta_column(self, data, **kwargs):
        return MetaColumn(**data)


class ColumnWrite(Schema):
    name = Str(required=False, validate=Regexp(Identifier.COMPILED_PATTERN))
    col_type = Str(required=False)
    nullable = Bool(required=False)
    generator_setting_id = Integer(required=False, allow_none=True)


class ColumnCreate(ColumnWrite):
    name = Str(validate=Regexp(Identifier.COMPILED_PATTERN))
    col_type = Str()
    nullable = Bool()
    generator_setting_id = Integer(allow_none=True)
    table_id = Integer()
