from marshmallow import Schema
from marshmallow.fields import Integer, Str, Nested, List, Bool, Dict, Raw, Float
from marshmallow.validate import OneOf


class MessageView(Schema):
    result = Str()
    message = Str()


class ColumnBriefView(Schema):
    id = Integer()
    name = Str()


class ColumnTableBriefView(Schema):
    id = Integer()
    table_id = Integer()
    name = Str()


class GeneratorSettingView(Schema):
    id = Integer()
    name = Str()
    params = Dict(keys=Str())
    null_frequency = Float()


class GeneratorSettingWrite(Schema):
    name = Str()
    params = Dict(keys=Str(), allow_none=True)
    null_frequency = Float(allow_none=True)


class ColumnView(Schema):
    id = Integer()
    name = Str()
    col_type = Str()
    nullable = Bool()
    generator_setting = Nested(GeneratorSettingView())


class ColumnWrite(Schema):
    name = Str()
    col_type = Str()
    nullable = Bool()
    generator_setting_id = Integer(allow_none=True)


class ColumnCreate(ColumnWrite):
    table_id = Integer()


class ConstraintView(Schema):
    id = Integer()
    name = Str()
    constraint_type = Str()
    constrained_columns = List(Nested(ColumnBriefView()))
    referenced_columns = List(Nested(ColumnTableBriefView()))
    check_expression = Str()


class TableView(Schema):
    id = Integer()
    name = Str()
    columns = List(Nested(ColumnView()))
    constraints = List(Nested(ConstraintView()))
    generator_settings = List(Nested(GeneratorSettingView()))


class TableWrite(Schema):
    name = Str()


class TableCreate(TableWrite):
    project_id = Integer()


class TableListView(Schema):
    items = List(Nested(TableView()))


class UserView(Schema):
    id = Integer()
    email = Str()


class UserAndTokenView(Schema):
    user = Nested(UserView())
    token = Str()


class PreviewView(Schema):
    tables = Dict(keys=Str(), values=List(Dict(keys=Str())))


class GeneratorParam(Schema):
    name = Str()
    value_type = Str()

    min_value = Raw()
    max_value = Raw()
    greater_equal_than = Str(allow_none=True)


class GeneratorView(Schema):
    name = Str()
    only_for_type = Str()
    supports_null = Bool()
    param_list = List(Nested(GeneratorParam()))


class GeneratorListView(Schema):
    items = List(Nested(GeneratorView))


class DataSourceView(Schema):
    id = Integer()

    file_name = Str()
    mime_type = Str()

    driver = Str()
    db = Str()

    usr = Str()
    host = Str()
    port = Integer()


class DataSourceDatabaseWrite(Schema):
    project_id = Integer()

    driver = Str()
    db = Str()

    usr = Str()
    pwd = Str()
    host = Str()
    port = Integer()


class DataSourceListView(Schema):
    items = List(Nested(DataSourceView()))


class ProjectView(Schema):
    id = Integer()
    name = Str()
    tables = List(Nested(TableView()))
    data_sources = List(Nested(DataSourceView()))


class ProjectListView(Schema):
    items = List(Nested(ProjectView()))


class TableCountsWrite(Schema):
    rows_by_table_name = Dict(keys=Str(), values=Integer())


class ExportFileRequestWrite(Schema):
    output_format = Str(validate=OneOf(['csv', 'json']))
    table_counts = Nested(TableCountsWrite)
