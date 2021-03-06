from marshmallow import Schema
from marshmallow.fields import Str, Integer, Nested, List


class DataSourceView(Schema):
    id = Integer()

    file_name = Str(allow_none=True)
    mime_type = Str(allow_none=True)

    driver = Str(allow_none=True)
    db = Str(allow_none=True)

    usr = Str(allow_none=True)
    host = Str(allow_none=True)
    port = Integer(allow_none=True)


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
