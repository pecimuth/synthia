from typing import List, Type

from core.service.exception import SomeError
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
