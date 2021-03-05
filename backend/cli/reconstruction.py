import json
from typing import Optional, Dict, Iterable, Tuple

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from web.view.project import SavedProject, SaveView


class ProjectReconstruction:
    def __init__(self, string_project: str):
        self._string_project = string_project
        self._raw_saved_project = None
        self._saved_project: Optional[SavedProject] = None

    def parse(self) -> SavedProject:
        self._raw_saved_project = json.loads(self._string_project)
        self._saved_project = SaveView().load(self._raw_saved_project)
        self._reconstruct_constraints()
        self._reconstruct_generators()
        return self._saved_project

    def _table_pairs(self) -> Iterable[Tuple[MetaTable, dict]]:
        return zip(self._saved_project.project.tables, self._raw_saved_project['project']['tables'])

    def _cols_by_id(self) -> Dict[int, MetaColumn]:
        col: Dict[int, MetaColumn] = {}
        for meta_table in self._saved_project.project.tables:
            for meta_column in meta_table.columns:
                col[meta_column.id] = meta_column
        return col

    def _reconstruct_constraints(self):
        col = self._cols_by_id()
        for meta_table, raw_table in self._table_pairs():
            for meta_constraint, raw_constraint in zip(meta_table.constraints, raw_table['constraints']):
                for constrained_column in raw_constraint['constrained_columns']:
                    meta_constraint.constrained_columns.append(col[constrained_column['id']])
                for referenced_column in raw_constraint['referenced_columns']:
                    meta_constraint.referenced_columns.append(col[referenced_column['id']])

    def _gens_by_id(self) -> Dict[int, GeneratorSetting]:
        gen: Dict[int, GeneratorSetting] = {}
        for meta_table in self._saved_project.project.tables:
            for generator_setting in meta_table.generator_settings:
                gen[generator_setting.id] = generator_setting
        return gen

    def _reconstruct_generators(self):
        gen = self._gens_by_id()
        for meta_table, raw_table in self._table_pairs():
            for meta_column, raw_column in zip(meta_table.columns, raw_table['columns']):
                generator_setting = raw_column['generator_setting']
                if generator_setting is not None:
                    meta_column.generator_setting = gen[generator_setting['id']]
