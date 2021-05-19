import datetime as dt
from typing import TypeVar, Optional

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.decorator import parameter
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.data_source.data_provider import DataProvider
from core.service.generation_procedure.database import GeneratedDatabase
from core.service.types import Types

OutputType = TypeVar('OutputType')


class FakerDateTimeGenerator(FakerGenerator[dt.datetime]):
    category = GeneratorCategory.DATETIME

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return Types.DATETIME


class FakerDateTimeStringGenerator(FakerGenerator[str]):
    category = GeneratorCategory.DATETIME

    @classmethod
    def only_for_type(cls) -> Optional[Types]:
        return Types.STRING


class DateStringGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    """Generated dates in a given format from 1970-1-1 until an end date."""

    provider = 'date'

    @parameter(allowed_values=['%Y-%m-%d', '%d/%m/%Y', '%d.%m.%Y'])
    def pattern(self) -> str:
        return '%Y-%m-%d'

    @parameter
    def end(self) -> dt.datetime:
        return dt.datetime(2021, 1, 1)

    @end.estimator
    def end(self, provider: DataProvider) -> dt.datetime:
        return provider.estimate_max()

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self.pattern, self.end)


class DateTime(RegisteredGenerator, FakerDateTimeGenerator):
    """Generate date times uniformly sampled from an interval."""

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


class TimeStringGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    """Generate random time in a format of choice."""

    provider = 'time'

    @parameter(allowed_values=['%H:%M:%S', '%H:%M', '%M:%S'])
    def pattern(self) -> str:
        return '%H:%M:%S'

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self.pattern)


class DayOfMonthGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    provider = 'day_of_month'


class DayOfWeekGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    """Generate English names of the days of the week."""

    provider = 'day_of_week'


class MonthGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    provider = 'month'


class MonthNameGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    """Generate English names of the month."""

    provider = 'month_name'


class TimeZoneGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    """Generate string denoting a canonical time zone from the tz database."""

    provider = 'timezone'


class YearGenerator(RegisteredGenerator, FakerDateTimeStringGenerator):
    provider = 'year'
