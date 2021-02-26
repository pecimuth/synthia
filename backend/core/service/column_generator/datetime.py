import datetime

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import ColumnGenerator
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class DatetimeGenerator(ColumnGenerator[datetime.datetime]):
    name = 'datetime'
    only_for_type = Types.DATETIME

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == Types.DATETIME

    def make_scalar(self, generated_database: GeneratedDatabase) -> datetime.datetime:
        return datetime.datetime.now()
