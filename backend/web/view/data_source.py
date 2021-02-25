from marshmallow import Schema
from marshmallow.fields import Str, Integer, Nested, List


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
