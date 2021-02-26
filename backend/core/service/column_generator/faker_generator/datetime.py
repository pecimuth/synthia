from datetime import datetime
from typing import TypeVar, Generic

from core.model.meta_column import MetaColumn
from core.service.column_generator.base import GeneratorCategory, RegisteredGenerator
from core.service.column_generator.faker_generator.base import FakerGenerator
from core.service.column_generator.params import ColumnGeneratorParam
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

    param_list = [
        ColumnGeneratorParam(
            name='pattern',
            value_type=Types.STRING,
            allowed_values=['%d/%m/%Y', '%Y-%m-%d', '%d.%m.%Y'],
            default_value='%d/%m/%Y'
        ),
        ColumnGeneratorParam(
            name='end',
            value_type=Types.DATETIME,
            default_value=datetime(2021, 1, 1),
        )
    ]

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self._params['pattern'], self._params['end'])

    def _estimate_params_with_provider(self, provider: DataProvider):
        self._params['end'] = provider.estimate_max() or self.param_list[1].default_value


class DateTime(RegisteredGenerator, FakerDateTimeGenerator[datetime]):
    name = 'datetime'
    provider = 'date_time_between'

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

    @classmethod
    def is_recommended_for(cls, meta_column: MetaColumn) -> bool:
        return True

    def make_scalar(self, generated_database: GeneratedDatabase) -> datetime:
        return self._functor(self._params['start'], self._params['end'])

    def _estimate_params_with_provider(self, provider: DataProvider):
        self._params['start'] = provider.estimate_min() or self.param_list[0].default_value
        self._params['end'] = provider.estimate_max() or self.param_list[1].default_value


class TimeStringGenerator(RegisteredGenerator, FakerDateTimeGenerator[str]):
    name = 'time_string'
    provider = 'time'
    only_for_type = Types.STRING

    param_list = [
        ColumnGeneratorParam(
            name='pattern',
            value_type=Types.STRING,
            allowed_values=['%H:%M:%S', '%H:%M', '%M:%S'],
            default_value='%H:%M:%S'
        )
    ]

    def make_scalar(self, generated_database: GeneratedDatabase) -> str:
        return self._functor(self._params['pattern'])


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
