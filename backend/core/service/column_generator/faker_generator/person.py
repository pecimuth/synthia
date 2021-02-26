from core.service.column_generator.base import GeneratorCategory, ColumnGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerPersonGenerator(FakerGenerator[str]):
    category = GeneratorCategory.PERSON
    only_for_type = Types.STRING


class NameGenerator(FakerPersonGenerator, ColumnGenerator[str]):
    name = 'name'


class FirstNameGenerator(FakerPersonGenerator, ColumnGenerator[str]):
    name = 'first_name'


class LastNameGenerator(FakerPersonGenerator, ColumnGenerator[str]):
    name = 'last_name'


class PhoneNumberGenerator(FakerPersonGenerator, ColumnGenerator[str]):
    name = 'phone_number'


class EmailGenerator(FakerPersonGenerator, ColumnGenerator[str]):
    name = 'email'
