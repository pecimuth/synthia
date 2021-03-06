import json

from core.service.output_driver.file_driver.base import FileOutputDriver
from core.service.types import json_serialize_default


class JsonOutputDriver(FileOutputDriver[str]):
    """Output file driver for JSON output."""

    mime_type = 'application/json'
    display_name = 'JSON'
    cli_command = 'json'

    def dump(self) -> str:
        return json.dumps(self._database.get_dict(),
                          indent=2,
                          sort_keys=True,
                          default=json_serialize_default)

    @classmethod
    def add_extension(cls, file_name_base: str) -> str:
        return '{}.json'.format(file_name_base)
