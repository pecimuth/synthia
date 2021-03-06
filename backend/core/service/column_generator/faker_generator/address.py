from typing import Optional

from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerAddressGenerator(FakerGenerator[str]):
    category = GeneratorCategory.ADDRESS

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return Types.STRING


class CityGenerator(RegisteredGenerator, FakerAddressGenerator):
    provider = 'city'


class CountryGenerator(RegisteredGenerator, FakerAddressGenerator):
    provider = 'country'


class CountryCodeGenerator(RegisteredGenerator, FakerAddressGenerator):
    """Generate country codes in the Alpha 2 format."""
    provider = 'country_code'


class PostcodeGenerator(RegisteredGenerator, FakerAddressGenerator):
    provider = 'postcode'


class StreetAddressGenerator(RegisteredGenerator, FakerAddressGenerator):
    provider = 'street_address'


class StreetNameGenerator(RegisteredGenerator, FakerAddressGenerator):
    provider = 'street_name'
