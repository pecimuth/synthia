from core.service.column_generator.base import GeneratorCategory, ColumnGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types


class FakerTextGenerator(FakerGenerator[str]):
    category = GeneratorCategory.TEXT
    only_for_type = Types.STRING


class WordGenerator(ColumnGenerator[str], FakerTextGenerator):
    name = 'word'


class TextGenerator(ColumnGenerator[str], FakerTextGenerator):
    name = 'text'

    param_list = [
        ColumnGeneratorParam(
            name='max_number_of_chars',
            value_type=Types.INTEGER,
            default_value=50,
            min_value=0,
            max_value=200
        )
    ]

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self._params['max_number_of_chars'])


class ParagraphGenerator(ColumnGenerator[str], FakerTextGenerator):
    name = 'paragraph'

    param_list = [
        ColumnGeneratorParam(
            name='number_of_sentences',
            value_type=Types.INTEGER,
            default_value=1,
            min_value=0,
            max_value=10
        )
    ]

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self._params['number_of_sentences'])
