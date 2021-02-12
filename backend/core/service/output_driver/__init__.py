from abc import ABC
from typing import List, Tuple, Iterable, Union, Dict

from sqlalchemy import Table

from core.model.meta_table import MetaTable
from core.model.project import Project
from core.service.deserializer import StructureDeserializer
from core.service.column_generator import GeneratedRow, GeneratedDatabase, GeneratedTable

MetaTableCount = Tuple[MetaTable, int]
MetaTableCounts = List[MetaTableCount]


class OutputDriver(ABC):
    is_interactive: bool

    def __init__(self, project: Project, meta_table_counts: MetaTableCounts):
        self._project = project
        self._meta_table_counts = meta_table_counts
        self._by_name: Dict[str, MetaTableCount] = {
            table.name: (table, count) for table, count in meta_table_counts
        }

        self._generated_database: Union[GeneratedDatabase, None] = None
        self._generated_table: Union[GeneratedTable, None] = None
        self._current_meta_table: Union[MetaTable, None] = None
        self._current_table: Union[Table, None] = None
        self._rows_left: int = 0

    def _on_generation_begin(self):
        self._generated_database = {}

    def _on_generation_end(self):
        self._current_table = None
        self._current_meta_table = None
        self._rows_left = 0
        self._generated_table = None

    def _on_next_table(self, table: Table, meta_table: MetaTable, n_rows: int):
        self._current_table = table
        self._current_meta_table = meta_table
        self._rows_left = n_rows
        self._generated_table = []
        self._generated_database[table.name] = self._generated_table

    def table_choices(self) -> Iterable[MetaTable]:
        deserializer = StructureDeserializer(self._project)
        meta = deserializer.deserialize()
        self._on_generation_begin()
        for table in meta.sorted_tables:
            if table.name not in self._by_name:
                continue
            self._on_next_table(table, *self._by_name[table.name])
            yield self._current_meta_table
        self._on_generation_end()

    def expects_next_row(self) -> bool:
        return self._rows_left > 0 and self._current_meta_table is not None

    def insert_row(self, row: GeneratedRow) -> GeneratedRow:
        self._rows_left -= 1
        self._generated_table.append(row)
        return row

    @property
    def generated_database(self) -> Union[GeneratedDatabase, None]:
        return self._generated_database

    @property
    def generated_table(self) -> GeneratedTable:
        return self._generated_table


class PreviewOutputDriver(OutputDriver):
    is_interactive = False
