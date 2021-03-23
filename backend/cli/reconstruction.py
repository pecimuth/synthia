from typing import Optional, Dict, Iterable, Tuple

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.model.meta_table import MetaTable
from web.view.project import SavedProject, SaveView


class ProjectReconstruction:
    """Reconstruct meta tables, columns, generators and constraints
    from a saved project, returned by the save project endpoint."""

    def __init__(self, raw_saved_project):
        self._raw_saved_project = raw_saved_project
        self._saved_project: Optional[SavedProject] = None

    def parse(self) -> SavedProject:
        """Parse and return the saved project."""
        self._saved_project = SaveView().load(self._raw_saved_project)
        self._reconstruct_constraints()
        self._reconstruct_generators()
        return self._saved_project

    def _table_pairs(self) -> Iterable[Tuple[MetaTable, dict]]:
        """Return pairs of recreated meta tables (without constraints)
        and the raw source dictionaries.
        """
        return zip(self._saved_project.project.tables, self._raw_saved_project['project']['tables'])

    def _cols_by_id(self) -> Dict[int, MetaColumn]:
        """Return dictionary of meta columns by ID."""
        col: Dict[int, MetaColumn] = {}
        for meta_table in self._saved_project.project.tables:
            for meta_column in meta_table.columns:
                col[meta_column.id] = meta_column
        return col

    def _reconstruct_constraints(self):
        """Create the constraints.

        When this method is called, the tables and columns must be assembled already.
        """
        col = self._cols_by_id()
        for meta_table, raw_table in self._table_pairs():
            for meta_constraint, raw_constraint in zip(meta_table.constraints, raw_table['constraints']):
                for col_id in raw_constraint['constrained_column_ids']:
                    meta_column = col[col_id]
                    meta_constraint.constrained_columns.append(meta_column)
                    meta_column.constraints.append(meta_constraint)
                for col_id in raw_constraint['referenced_column_ids']:
                    meta_column = col[col_id]
                    meta_constraint.referenced_columns.append(meta_column)

    def _gens_by_id(self) -> Dict[int, GeneratorSetting]:
        """Return dictionary of generator settings by ID.

        The generator must come from the meta tables, where they are created
        by the deserializer (post load).
        """
        gen: Dict[int, GeneratorSetting] = {}
        for meta_table in self._saved_project.project.tables:
            for generator_setting in meta_table.generator_settings:
                gen[generator_setting.id] = generator_setting
        return gen

    def _reconstruct_generators(self):
        """Assign real generator setting instances to columns.

        The generator setting instances are created on table basis first.
        """
        gen = self._gens_by_id()
        for meta_table in self._saved_project.project.tables:
            for meta_column in meta_table.columns:
                if meta_column.generator_setting_id is not None:
                    meta_column.generator_setting = gen[meta_column.generator_setting_id]
