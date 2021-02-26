from core.service.column_generator import ColumnGenerator
from core.service.column_generator.base import GeneratorCategory
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.types import Types


class FakerAddressGenerator(FakerGenerator[str]):
    category = GeneratorCategory.ADDRESS
    only_for_type = Types.STRING


class CityGenerator(ColumnGenerator[str], FakerAddressGenerator):
    name = 'city'


class CountryGenerator(ColumnGenerator[str], FakerAddressGenerator):
    name = 'country'


class CountryCodeGenerator(ColumnGenerator[str], FakerAddressGenerator):
    name = 'country_code'


class PostcodeGenerator(ColumnGenerator[str], FakerAddressGenerator):
    name = 'postcode'


class StreetAddressGenerator(ColumnGenerator[str], FakerAddressGenerator):
    name = 'street_address'


class StreetNameGenerator(ColumnGenerator[str], FakerAddressGenerator):
    name = 'street_name'
