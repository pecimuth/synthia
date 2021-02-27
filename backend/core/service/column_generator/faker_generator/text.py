from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.decorator import parameter
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class FakerTextGenerator(FakerGenerator[str]):
    category = GeneratorCategory.TEXT
    only_for_type = Types.STRING


class WordGenerator(RegisteredGenerator, FakerTextGenerator):
    name = 'word'


class TextGenerator(RegisteredGenerator, FakerTextGenerator):
    name = 'text'

    @parameter(min_value=0, max_value=200)
    def max_number_of_chars(self) -> int:
        return 50

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self.max_number_of_chars)


class ParagraphGenerator(RegisteredGenerator, FakerTextGenerator):
    name = 'paragraph'

    @parameter(min_value=0, max_value=10)
    def number_of_sentences(self) -> int:
        return 1

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self.number_of_sentences)
