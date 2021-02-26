from core.service.column_generator import ColumnGenerator
from core.service.column_generator.base import GeneratorCategory
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerAddressGenerator(FakerGenerator[str]):
    category = GeneratorCategory.ADDRESS
    only_for_type = Types.STRING


class CityGenerator(FakerAddressGenerator, ColumnGenerator[str]):
    name = 'city'


class CountryGenerator(FakerAddressGenerator, ColumnGenerator[str]):
    name = 'country'


class CountryCodeGenerator(FakerAddressGenerator, ColumnGenerator[str]):
    name = 'country_code'


class PostcodeGenerator(FakerAddressGenerator, ColumnGenerator[str]):
    name = 'postcode'


class StreetAddressGenerator(FakerAddressGenerator, ColumnGenerator[str]):
    name = 'street_address'


class StreetNameGenerator(FakerAddressGenerator, ColumnGenerator[str]):
    name = 'street_name'
