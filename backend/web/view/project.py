from marshmallow import Schema
from marshmallow.fields import Integer, Str, Nested, List, Dict
from marshmallow.validate import OneOf

from core.service.output_driver.file_driver.facade import FileOutputDriverFacade
from web.view.data_source import DataSourceView
from web.view.table import TableView


class ProjectView(Schema):
    id = Integer()
    name = Str()
    tables = List(Nested(TableView()))
    data_sources = List(Nested(DataSourceView()))


class ProjectListView(Schema):
    items = List(Nested(ProjectView()))


class ExportRequisitionRow(Schema):
    table_name = Str()
    row_count = Integer()
    seed = Integer()


class ExportRequisitionWrite(Schema):
    rows = List(Nested(ExportRequisitionRow()))


class ExportFileRequisitionWrite(ExportRequisitionWrite):
    driver_name = Str(validate=OneOf(FileOutputDriverFacade.get_driver_name_list()))


class PreviewView(Schema):
    tables = Dict(keys=Str(), values=List(Dict(keys=Str())))
