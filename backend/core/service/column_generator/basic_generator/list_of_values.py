from typing import Any, Optional

from core.model.generator_setting import GeneratorSetting
from core.service.column_generator.base import RegisteredGenerator, SingleColumnGenerator
from core.service.column_generator.decorator import parameter
from core.service.data_source.data_provider import DataProvider
from core.service.exception import SomeError, ColumnGeneratorError
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types, get_type_conversion_functor, DATETIME_FORMAT_NICE


class ListOfValuesGenerator(RegisteredGenerator, SingleColumnGenerator[Any]):
    """Select a random value from a list of values.

    The list contains values separated with a customizable separator.
    """

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        self._values: Optional[tuple] = None

    @parameter
    def list_of_values(self) -> str:
        return '1,2,3'

    @list_of_values.estimator
    def list_of_values(self, provider: DataProvider) -> str:
        return self.separator.join(map(str, provider.scalar_data_not_none()))

    @parameter
    def separator(self) -> str:
        return ','

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return None

    def seed(self, seed: Optional[float]):
        super().seed(seed)
        self._values = []
        col_type = self._meta_column.col_type
        converter = get_type_conversion_functor(self._meta_column.col_type, DATETIME_FORMAT_NICE)
        for value in self.list_of_values.split(self.separator):
            try:
                self._values.append(converter(value))
            except (SomeError, ValueError):
                raise ColumnGeneratorError(
                    'conversion of the value `{}` to {} failed'.format(value, col_type),
                    self._meta_column
                )
        if not self._values:
            raise ColumnGeneratorError('the list of values is empty', self._meta_column)

    def make_scalar(self, generated_database: GeneratedDatabase) -> Any:
        return self._random.choice(self._values)
