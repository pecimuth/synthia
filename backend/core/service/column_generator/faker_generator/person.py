from typing import Optional

from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerPersonGenerator(FakerGenerator[str]):
    category = GeneratorCategory.PERSON

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return Types.STRING


class FirstNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    """Generate human first names."""

    provider = 'first_name'


class LastNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    """Generate human last names."""

    provider = 'last_name'


class PhoneNumberGenerator(RegisteredGenerator, FakerPersonGenerator):
    """Generate phone numbers in various formats."""

    provider = 'phone_number'


class EmailGenerator(RegisteredGenerator, FakerPersonGenerator):
    provider = 'email'


class UserNameGenerator(RegisteredGenerator, FakerPersonGenerator):
    """Generate realistic user names."""

    provider = 'user_name'


class NameGenerator(RegisteredGenerator, FakerPersonGenerator):
    """Generate human names."""

    provider = 'name'
