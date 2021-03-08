from typing import List, Type

from core.service.exception import SomeError
from core.service.output_driver import OutputDriver
from core.service.output_driver.file_driver.base import FileOutputDriver


class FileOutputDriverFacade:

    @staticmethod
    def get_driver_list() -> List[Type[FileOutputDriver]]:
        return FileOutputDriver.__subclasses__()

    @staticmethod
    def get_driver_name_list() -> List[str]:
        return [
            driver.driver_name()
            for driver in FileOutputDriver.__subclasses__()
        ]

    @staticmethod
    def make_driver(driver_name: str) -> FileOutputDriver:
        for driver in FileOutputDriver.__subclasses__():
            if driver.driver_name() == driver_name:
                return driver()
        raise SomeError('Invalid file driver name')

    @staticmethod
    def get_driver_by_cli_command(cli_command: str) -> Type[OutputDriver]:
        for driver in OutputDriver.__subclasses__():
            if driver.cli_command == cli_command:
                return driver
        raise SomeError('Invalid driver cli command')
