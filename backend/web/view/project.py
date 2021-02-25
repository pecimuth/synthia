from marshmallow import Schema
from marshmallow.fields import Integer, Str, Nested, List, Dict
from marshmallow.validate import OneOf

from web.view.data_source import DataSourceView
from web.view.table import TableView


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
    table_counts = Nested(TableCountsWrite())


class PreviewView(Schema):
    tables = Dict(keys=Str(), values=List(Dict(keys=Str())))
