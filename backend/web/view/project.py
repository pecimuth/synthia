from dataclasses import dataclass

from marshmallow import Schema, post_load
from marshmallow.fields import Int, Str, Nested, List, Dict
from marshmallow.validate import OneOf, Range

from core.model.project import Project
from core.service.generation_procedure.requisition import ExportRequisition, ExportRequisitionRow
from core.service.output_driver.file_driver.facade import FileOutputDriverFacade
from web.view.data_source import DataSourceView
from web.view.table import TableView, SavedTableView


class ProjectView(Schema):
    id = Int()
    name = Str()
    tables = List(Nested(TableView()))
    data_sources = List(Nested(DataSourceView()))


class ProjectWrite(Schema):
    name = Str()


class ProjectListView(Schema):
    items = List(Nested(ProjectView()))


class ExportRequisitionRowView(Schema):
    table_name = Str()
    row_count = Int(validate=Range(min=1))
    seed = Int(allow_none=True)

    @post_load
    def make_row(self, data, **kwargs):
        return ExportRequisitionRow(**data)


class ExportRequisitionView(Schema):
    rows = List(Nested(ExportRequisitionRowView()))

    @post_load
    def make_requisition(self, data, **kwargs):
        return ExportRequisition(data['rows'])


class ExportFileRequisitionView(ExportRequisitionView):
    driver_name = Str(validate=OneOf(FileOutputDriverFacade.get_driver_name_list()))

    @post_load
    def make_requisition(self, data, **kwargs):
        return ExportRequisition(data['rows']), data['driver_name']


class PreviewView(Schema):
    tables = Dict(keys=Str(), values=List(Dict(keys=Str())))


class SavedProjectView(Schema):
    id = Int()
    name = Str()
    tables = List(Nested(SavedTableView()))

    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)


@dataclass
class SavedProject:
    project: Project
    requisition: ExportRequisition


class SaveView(Schema):
    project = Nested(SavedProjectView())
    requisition = Nested(ExportRequisitionView())

    @post_load
    def make_saved_project(self, data, **kwargs):
        return SavedProject(**data)
