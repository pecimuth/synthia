from core.model.data_source import DataSource
from core.model.meta_column import MetaColumn
from core.service.data_source.identifier import Identifier


class SomeError(Exception):
    def __init__(self, message: str):
        self.message = message


class GeneratorRegistrationError(SomeError):
    def __init__(self):
        super().__init__('registered generator must be a column generator')


class DataSourceError(SomeError):
    def __init__(self, message: str, data_source: DataSource):
        super().__init__(message)
        self.data_source = data_source


class DataSourceIdentifierError(DataSourceError):
    def __init__(self, message: str, data_source: DataSource, identifier: Identifier):
        super().__init__(message, data_source)
        self.identifier = identifier


class ColumnGeneratorError(SomeError):
    def __init__(self, message: str, meta_column: MetaColumn):
        super().__init__(message)
        self.meta_column = meta_column
