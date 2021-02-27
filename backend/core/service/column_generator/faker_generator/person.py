from typing import Optional

from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerPersonGenerator(FakerGenerator[str]):
    category = GeneratorCategory.PERSON

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return Types.STRING


class NameGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'provider'


class FirstNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'first_provider'


class LastNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'last_provider'


class PhoneNumberGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'phone_number'


class EmailGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'email'


class UserNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'user_provider'
