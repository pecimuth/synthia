from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerAddressGenerator(FakerGenerator[str]):
    category = GeneratorCategory.ADDRESS
    only_for_type = Types.STRING


class CityGenerator(RegisteredGenerator, FakerAddressGenerator):
    name = 'city'


class CountryGenerator(RegisteredGenerator, FakerAddressGenerator):
    name = 'country'


class CountryCodeGenerator(RegisteredGenerator, FakerAddressGenerator):
    name = 'country_code'


class PostcodeGenerator(RegisteredGenerator, FakerAddressGenerator):
    name = 'postcode'


class StreetAddressGenerator(RegisteredGenerator, FakerAddressGenerator):
    name = 'street_address'


class StreetNameGenerator(RegisteredGenerator, FakerAddressGenerator):
    name = 'street_name'
