from marshmallow import Schema
from marshmallow.fields import Integer, Str, List, Nested

from web.view.column import ColumnBriefView, ColumnTableBriefView, ColumnView
from web.view.generator import GeneratorSettingView


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
