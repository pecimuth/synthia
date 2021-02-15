import random
import string

from core.model.meta_column import MetaColumn
from core.service.column_generator import ColumnGeneratorParam
from core.service.column_generator.base import ColumnGeneratorBase
from core.service.generation_procedure.database import GeneratedDatabase


class StringGenerator(ColumnGeneratorBase[str]):
    name = 'string'
    param_list = [
        ColumnGeneratorParam(name='length', value_type='number', default_value=10)
    ]

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return meta_column.col_type == 'VARCHAR'

    def make_value(self, generated_database: GeneratedDatabase) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(self._params['length']))
