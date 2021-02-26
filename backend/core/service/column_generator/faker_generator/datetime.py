from datetime import datetime
from typing import TypeVar, Generic

from core.service.column_generator.base import GeneratorCategory, ColumnGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.column_generator.params import ColumnGeneratorParam
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types

OutputType = TypeVar('OutputType')


class FakerDateTimeGenerator(Generic[OutputType], FakerGenerator[OutputType]):
    category = GeneratorCategory.DATETIME
    only_for_type = Types.DATETIME


class DateGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'date'
    only_for_type = Types.STRING


class DateBetween(FakerDateTimeGenerator[datetime], ColumnGenerator[datetime]):
    name = 'date_between'
    provider = 'date_between_dates'

    param_list = [
        ColumnGeneratorParam(
            name='start',
            value_type=Types.DATETIME,
            default_value=datetime(1970, 1, 1)
        ),
        ColumnGeneratorParam(
            name='end',
            value_type=Types.DATETIME,
            default_value=datetime(2021, 1, 1),
            greater_equal_than='start'
        )
    ]

    def make_scalar(self, generated_database: GeneratedDatabase) -> OutputType:
        return self._functor(self._params['start'], self._params['end'])


class DateOfBirthGenerator(FakerDateTimeGenerator[datetime], ColumnGenerator[datetime]):
    name = 'date_of_birth'


class DayOfMonthGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'day_of_month'
    only_for_type = Types.STRING


class DayOfWeekGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'day_of_week'
    only_for_type = Types.STRING


class FutureDateGenerator(FakerDateTimeGenerator[datetime], ColumnGenerator[datetime]):
    name = 'future_date'


class MonthGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'month'
    only_for_type = Types.STRING


class MonthNameGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'month_name'
    only_for_type = Types.STRING


class TimeZoneGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'timezone'
    only_for_type = Types.STRING


class UnixTimeGenerator(FakerDateTimeGenerator[int], ColumnGenerator[int]):
    name = 'unix_time'
    only_for_type = Types.INTEGER


class YearGenerator(FakerDateTimeGenerator[str], ColumnGenerator[str]):
    name = 'year'
    only_for_type = Types.STRING
