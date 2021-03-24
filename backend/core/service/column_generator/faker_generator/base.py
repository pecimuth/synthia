from typing import TypeVar, Generic

from faker import Faker

from core.model.generator_setting import GeneratorSetting
from core.service.column_generator.base import SingleColumnGenerator
from core.service.generation_procedure.database import GeneratedDatabase

OutputType = TypeVar('OutputType')


class FakerGenerator(Generic[OutputType], SingleColumnGenerator[OutputType]):
    """Base Faker generator. Adapts Faker generators to our generators."""

    provider: str
    """The name of the Faker provider."""

    def __init__(self, generator_setting: GeneratorSetting):
        super().__init__(generator_setting)
        self._fake: Faker = Faker()
        self._functor = getattr(self._fake, self.provider)

    def seed(self, seed: float):
        """Seed the Faker generator instance."""
        self._fake.seed_instance(seed)

    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        """Call the Faker generator instance."""
        return self._functor()
