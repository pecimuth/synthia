from marshmallow import Schema, post_load
from marshmallow.fields import Integer, Str, List, Nested, Method
from marshmallow.validate import Regexp

from core.model.meta_constraint import MetaConstraint
from core.model.meta_table import MetaTable
from core.service.data_source.identifier import Identifier
from web.view.column import ColumnBriefView, ColumnTableBriefView, ColumnView, SavedColumnView, ColumnIdView
from web.view.generator import GeneratorSettingView


class ConstraintView(Schema):
    id = Integer()
    name = Str(allow_none=True)
    constraint_type = Str()
    constrained_columns = List(Nested(ColumnBriefView()))
    referenced_columns = List(Nested(ColumnTableBriefView()))
    check_expression = Str(allow_none=True)

    @post_load
    def make_meta_constraint(self, data, **kwargs):
        return MetaConstraint(
            id=data['id'],
            name=data['name'],
            constraint_type=data['constraint_type'],
            check_expression=data['check_expression']
        )


class TableView(Schema):
    id = Integer()
    name = Str()
    columns = List(Nested(ColumnView()))
    constraints = List(Nested(ConstraintView()))
    generator_settings = List(Nested(GeneratorSettingView()))

    @post_load
    def make_meta_table(self, data, **kwargs):
        return MetaTable(**data)


class TableWrite(Schema):
    name = Str(validate=Regexp(Identifier.COMPILED_PATTERN))


class TableCreate(TableWrite):
    project_id = Integer()


class TableListView(Schema):
    items = List(Nested(TableView()))

    @post_load
    def make_table_list(self, data, **kwargs):
        return list(data['items'])


class SavedConstraintView(Schema):
    id = Integer()
    name = Str(allow_none=True)
    constraint_type = Str()
    constrained_column_ids = Method('get_constrained_column_ids', 'identity')
    referenced_column_ids = Method('get_referenced_column_ids', 'identity')
    check_expression = Str(allow_none=True)

    def get_constrained_column_ids(self, obj):
        return list(map(lambda column: column.id, obj.constrained_columns))

    def get_referenced_column_ids(self, obj):
        return list(map(lambda column: column.id, obj.referenced_columns))

    def identity(self, value):
        return value

    @post_load
    def make_meta_constraint(self, data, **kwargs):
        return MetaConstraint(
            id=data['id'],
            name=data['name'],
            constraint_type=data['constraint_type'],
            check_expression=data['check_expression']
        )


class SavedTableView(Schema):
    id = Integer()
    name = Str()
    columns = List(Nested(SavedColumnView()))
    constraints = List(Nested(SavedConstraintView()))
    generator_settings = List(Nested(GeneratorSettingView()))

    @post_load
    def make_meta_table(self, data, **kwargs):
        return MetaTable(**data)
