import datetime

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class DatetimeGenerator(ColumnGeneratorBase[datetime.datetime]):
    name = 'datetime'

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == Types.DATETIME

    def make_value(self, generated_database: GeneratedDatabase) -> datetime.datetime:
        return datetime.datetime.now()
