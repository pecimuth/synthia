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


class TableView(Schema):
    id = Integer()
    name = Str()
    columns = List(Nested(ColumnView()))


class TableListView(Schema):
    items = List(Nested(TableView()))


class ProjectView(Schema):
    id = Integer()
    name = Str()
    tables = List(Nested(TableView()))


class ProjectListView(Schema):
    items = List(Nested(ProjectView()))


class UserView(Schema):
    id = Integer()
    email = Str()


class TablePreviewView(Schema):
    rows = List(Dict(keys=Str()))
