import random
import string

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import RegisteredGenerator, SingleColumnGenerator
from core.service.column_generator.decorator import parameter
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase


class StringGenerator(RegisteredGenerator, SingleColumnGenerator[str]):

    @parameter(min_value=1)
    def min_length(self) -> int:
        return 1

    @parameter(max_value=100, greater_equal_than='min_length')
    def max_length(self) -> int:
        return 10

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        length = random.randint(self.min_length, self.max_length)
        return self._random_string_of_length(length)

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return True

    @classmethod
    def _random_string_of_length(cls, length: int) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def _estimate_params_with_provider(self, provider: DataProvider):
        min_len = None
        max_len = None
        for sample in provider.scalar_data_not_none():
            if min_len is None or len(sample) < min_len:
                min_len = len(sample)
            if max_len is None or len(sample) > max_len:
                max_len = len(sample)
        self.min_length = min_len or 1
        self.max_length = max_len or 10
