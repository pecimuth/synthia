from marshmallow import Schema
from marshmallow.fields import Integer, Str, Nested, List, Bool, Dict, Raw
from marshmallow.validate import OneOf


class MessageView(Schema):
    result = Str()
    message = Str()


class ColumnView(Schema):
    id = Integer()
    name = Str()
    col_type = Str()
    primary_key = Bool()
    nullable = Bool()
    foreign_key = Str()
    generator_name = Str()
    generator_params = Dict(keys=Str())


class ColumnWrite(Schema):
    generator_name = Str()
    generator_params = Dict(keys=Str(), allow_none=True)


class TableView(Schema):
    id = Integer()
    name = Str()
    columns = List(Nested(ColumnView()))
    row_count = Integer()


class TableWrite(Schema):
    row_count = Integer()


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
