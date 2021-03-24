from typing import List, Type

from core.service.exception import SomeError
from core.service.output_driver.file_driver.base import FileOutputDriver


class FileOutputDriverFacade:
    """List output file drivers and create them by name."""

    @staticmethod
    def get_driver_list() -> List[Type[FileOutputDriver]]:
        """Return list of output file drivers (types)."""
        return FileOutputDriver.__subclasses__()

    @staticmethod
    def get_driver_name_list() -> List[str]:
        """Return list of output file driver identifiers."""
        return [
            driver.driver_name()
            for driver in FileOutputDriver.__subclasses__()
        ]

    @staticmethod
    def make_driver(driver_name: str) -> FileOutputDriver:
        """Make output file driver from an identifier."""
        for driver in FileOutputDriver.__subclasses__():
            if driver.driver_name() == driver_name:
                return driver()
        raise SomeError('Invalid file driver name')
