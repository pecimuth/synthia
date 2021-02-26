from core.service.column_generator.base import GeneratorCategory, ColumnGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerPersonGenerator(FakerGenerator[str]):
    category = GeneratorCategory.PERSON
    only_for_type = Types.STRING


class NameGenerator(ColumnGenerator[str], FakerPersonGenerator):
    name = 'name'


class FirstNameGenerator(ColumnGenerator[str], FakerPersonGenerator):
    name = 'first_name'


class LastNameGenerator(ColumnGenerator[str], FakerPersonGenerator):
    name = 'last_name'


class PhoneNumberGenerator(ColumnGenerator[str], FakerPersonGenerator):
    name = 'phone_number'


class EmailGenerator(ColumnGenerator[str], FakerPersonGenerator):
    name = 'email'


class UserNameGenerator(ColumnGenerator[str], FakerPersonGenerator):
    name = 'user_name'
