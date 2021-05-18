from marshmallow import Schema, post_load
from marshmallow.fields import Int, Str, Bool, Nested
from marshmallow.validate import Regexp

from core.model.meta_column import MetaColumn
from core.service.data_source.identifier import Identifier
from web.view.generator import GeneratorSettingView


class ColumnIdView(Schema):
    id = Int()

    @post_load
    def make_meta_column(self, data, **kwargs):
        return MetaColumn(**data)


class ColumnBriefView(Schema):
    id = Int()
    name = Str()


class TableBriefView(Schema):
    id = Int()
    name = Str()


class ColumnTableBriefView(Schema):
    id = Int()
    name = Str()
    table = Nested(TableBriefView())


class ColumnView(Schema):
    id = Int()
    name = Str()
    col_type = Str()
    nullable = Bool()
    generator_setting = Nested(GeneratorSettingView())
    reflected_column_idf = Str()

    @post_load
    def make_meta_column(self, data, **kwargs):
        return MetaColumn(**data)


class ColumnWrite(Schema):
    name = Str(required=False, validate=Regexp(Identifier.COMPILED_PATTERN))
    col_type = Str(required=False)
    nullable = Bool(required=False)
    generator_setting_id = Int(required=False, allow_none=True)


class ColumnCreate(ColumnWrite):
    name = Str(validate=Regexp(Identifier.COMPILED_PATTERN))
    col_type = Str()
    nullable = Bool()
    generator_setting_id = Int(allow_none=True)
    table_id = Int()


class SavedColumnView(Schema):
    id = Int()
    name = Str()
    col_type = Str()
    nullable = Bool()
    generator_setting_id = Int()

    @post_load
    def make_meta_column(self, data, **kwargs):
        return MetaColumn(**data)
