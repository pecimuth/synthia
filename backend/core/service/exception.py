from core.model.data_source import DataSource
from core.model.generator_setting import GeneratorSetting
from core.model.meta_column import MetaColumn


class SomeError(Exception):
    def __init__(self, message: str):
        self.message = message


class DatabaseConnectionError(SomeError):
    def __init__(self):
        super().__init__('Could not connect to the database')


class FatalDatabaseError(SomeError):
    def __init__(self):
        super().__init__('Fatal database error')


class FileNotAllowedError(SomeError):
    def __init__(self):
        super().__init__('File not allowed')


class GeneratorRegistrationError(SomeError):
    def __init__(self):
        super().__init__('Registered generator must be a column generator')


class InvalidPasswordError(SomeError):
    def __init__(self):
        super().__init__('Please choose a different password')


class GeneratorSettingError(SomeError):
    def __init__(self, message: str, generator_setting: GeneratorSetting):
        super().__init__('{} ({} generator {})'.format(message,
                                                       generator_setting.name,
                                                       generator_setting.id))
        self.generator_setting = generator_setting


class DataSourceError(SomeError):
    def __init__(self, message: str, data_source: DataSource):
        super().__init__(message)
        self.data_source = data_source


class DatabaseNotReadable(DataSourceError):
    def __init__(self, data_source: DataSource):
        super().__init__('Unable to reflect the database', data_source)


class DataSourceIdentifierError(DataSourceError):
    def __init__(self, message: str, data_source: DataSource, identifier: str):
        super().__init__(message, data_source)
        self.identifier = identifier


class ColumnError(SomeError):
    def __init__(self, message: str, meta_column: MetaColumn):
        super().__init__('Column `{}`: {}'.format(meta_column.name, message))
        self.meta_column = meta_column


class ColumnGeneratorError(ColumnError):
    pass


class ColumnGeneratorNotAssignableError(ColumnGeneratorError):
    def __init__(self, meta_column: MetaColumn):
        super().__init__('the generator is not assignable to this column', meta_column)


class MalformedIdentifierError(SomeError):
    def __init__(self, identifier: str):
        super().__init__('Malformed identifier: `{}`'.format(identifier))


class RequisitionMissingReferenceError(SomeError):
    def __init__(self, included_table: str, ref_table: str):
        super().__init__('The table `{}` references the table `{}`, but it is not included in the export'
                         .format(included_table, ref_table))
