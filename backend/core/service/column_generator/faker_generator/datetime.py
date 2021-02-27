import datetime as dt
from typing import TypeVar, Generic

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.decorator import parameter
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types

OutputType = TypeVar('OutputType')


class FakerDateTimeGenerator(Generic[OutputType], FakerGenerator[OutputType]):
    category = GeneratorCategory.DATETIME
    only_for_type = Types.DATETIME


class DateStringGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'date_string'
    provider = 'date'
    only_for_type = Types.STRING

    @parameter(allowed_values=['%d/%m/%Y', '%Y-%m-%d', '%d.%m.%Y'])
    def pattern(self) -> str:
        return '%d/%m/%Y'

    @parameter
    def end(self) -> dt.datetime:
        return dt.datetime(2021, 1, 1)

    @end.estimator
    def end(self, provider: DataProvider) -> dt.datetime:
        return provider.estimate_max()

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self.pattern, self.end)


class DateTime(RegisteredGenerator, FakerDateTimeGenerator[dt.datetime]):
    name = 'datetime'
    provider = 'date_time_between'

    @parameter
    def start(self) -> dt.datetime:
        return dt.datetime(1970, 1, 1)

    @parameter(greater_equal_than='start')
    def end(self) -> dt.datetime:
        return dt.datetime(2021, 1, 1)

    @start.estimator
    def start(self, provider: DataProvider) -> dt.datetime:
        return provider.estimate_min()

    @end.estimator
    def end(self, provider: DataProvider) -> dt.datetime:
        return provider.estimate_max()

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return True

    def make_scalar(self, generated_database: GeneratedDatabase) -> dt.datetime:
        return self._functor(self.start, self.end)


class TimeStringGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'time_string'
    provider = 'time'
    only_for_type = Types.STRING

    @parameter(allowed_values=['%H:%M:%S', '%H:%M', '%M:%S'])
    def pattern(self) -> str:
        return '%H:%M:%S'

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self.pattern)


class DayOfMonthGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'day_of_month'
    only_for_type = Types.STRING


class DayOfWeekGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'day_of_week'
    only_for_type = Types.STRING


class MonthGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'month'
    only_for_type = Types.STRING


class MonthNameGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'month_name'
    only_for_type = Types.STRING


class TimeZoneGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'timezone'
    only_for_type = Types.STRING


class UnixTimeGenerator(RegisteredGenerator, FakerDateTimeGenerator[int]):
    name = 'unix_time'
    only_for_type = Types.INTEGER


class YearGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'year'
    only_for_type = Types.STRING
