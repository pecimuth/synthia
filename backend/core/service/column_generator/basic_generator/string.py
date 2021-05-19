import string

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import RegisteredGenerator, SingleColumnGenerator
from core.service.column_generator.decorator import parameter
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase


class StringGenerator(RegisteredGenerator, SingleColumnGenerator[str]):
    """Generate strings of ASCII letters of random length.
    The length is sampled uniformly from a closed interval.
    """

    @parameter(min_value=1)
    def min_length(self) -> int:
        return 1

    @parameter(max_value=100, greater_equal_than='min_length')
    def max_length(self) -> int:
        return 10

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        length = self._random.randint(self.min_length, self.max_length)
        return self._random_string_of_length(length)

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return True

    def _random_string_of_length(self, length: int) -> str:
        """Return a random string of given length."""
        sequence = (self._random.choice(string.ascii_letters) for _ in range(length))
        return ''.join(sequence)

    def estimate_params(self, provider: DataProvider):
        super().estimate_params(provider)
        min_len = None
        max_len = None
        for sample in provider.scalar_data_not_none():
            if min_len is None or len(sample) < min_len:
                min_len = len(sample)
            if max_len is None or len(sample) > max_len:
                max_len = len(sample)
        self.min_length = min_len or 1
        self.max_length = max_len or 10
