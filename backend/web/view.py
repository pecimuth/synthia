from marshmallow import Schema
from marshmallow.fields import Integer, Str, Nested, List, Bool, Dict


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


class TablePreviewView(Schema):
    rows = List(Dict(keys=Str()))


class GeneratorParam(Schema):
    name = Str()
    value_type = Str()


class GeneratorView(Schema):
    name = Str()
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
