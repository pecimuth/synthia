import datetime

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.generation_procedure.database import GeneratedDatabase


class DatetimeGenerator(ColumnGeneratorBase[datetime.datetime]):
    name = 'datetime'

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'DATETIME'

    def make_value(self, generated_database: GeneratedDatabase) -> datetime.datetime:
        return datetime.datetime.now()
