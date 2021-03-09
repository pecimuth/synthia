from marshmallow import Schema
from marshmallow.fields import Str, Integer, Nested, List
from marshmallow.validate import OneOf

from core.service.data_source import DataSourceConstants


class DataSourceView(Schema):
    id = Integer()

    file_name = Str(allow_none=True)
    mime_type = Str(allow_none=True)

    driver = Str(allow_none=True)
    db = Str(allow_none=True)

    usr = Str(allow_none=True)
    host = Str(allow_none=True)
    port = Integer(allow_none=True)


class DataSourceDatabaseCreate(Schema):
    project_id = Integer()

    driver = Str(validate=OneOf([DataSourceConstants.DRIVER_POSTGRES]))
    db = Str()

    usr = Str()
    pwd = Str()
    host = Str()
    port = Integer()


class DataSourceDatabaseWrite(Schema):
    driver = Str(validate=OneOf([DataSourceConstants.DRIVER_POSTGRES]), required=False)
    db = Str(required=False)

    usr = Str(required=False)
    pwd = Str(required=False)
    host = Str(required=False)
    port = Integer(required=False)


class DataSourceListView(Schema):
    items = List(Nested(DataSourceView()))
