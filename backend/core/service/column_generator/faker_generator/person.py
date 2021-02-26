from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerPersonGenerator(FakerGenerator[str]):
    category = GeneratorCategory.PERSON
    only_for_type = Types.STRING


class NameGenerator(RegisteredGenerator, FakerPersonGenerator):
    name = 'name'


class FirstNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    name = 'first_name'


class LastNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    name = 'last_name'


class PhoneNumberGenerator(RegisteredGenerator, FakerPersonGenerator):
    name = 'phone_number'


class EmailGenerator(RegisteredGenerator, FakerPersonGenerator):
    name = 'email'


class UserNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    name = 'user_name'
