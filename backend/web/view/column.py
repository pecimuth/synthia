from marshmallow import Schema
from marshmallow.fields import Integer, Str, Bool, Nested

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


class ColumnWrite(Schema):
    name = Str(required=False)
    col_type = Str(required=False)
    nullable = Bool(required=False)
    generator_setting_id = Integer(required=False, allow_none=True)


class ColumnCreate(ColumnWrite):
    name = Str()
    col_type = Str()
    nullable = Bool()
    generator_setting_id = Integer(allow_none=True)
