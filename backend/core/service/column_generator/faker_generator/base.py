from typing import TypeVar, Generic, Set

from faker import Faker

from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')


class FakerGenerator(Generic[OutputType]):
    name: str
    provider: str
    column_names: Set[str]

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        self._fake = Faker()
        if not hasattr(self, 'provider'):
            self.provider = self.name
        self._functor = getattr(self._fake, self.provider)

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        normal = meta_column.name.lower()
        if hasattr(cls, 'column_names'):
            return normal in cls.column_names
        return normal == cls.name

    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        return self._functor()
