import json
from typing import AnyStr, Tuple

from cli.controller import CommandLineController
from core.service.mock_schema import mock_book_author_publisher
from core.service.output_driver.file_driver.json_file import JsonOutputDriver


class TestCli:
    """Test the CLI functionality."""

    def test_json(self,
                  saved_mock_project_file: Tuple[int, AnyStr],
                  temp_output_file: Tuple[int, AnyStr]):
        """Test JSON data generation."""
        # project file
        project_fd, project_file_path = saved_mock_project_file
        # output file
        output_fd, output_file_path = temp_output_file

        # run the generator
        controller = CommandLineController()
        controller.execute([
            JsonOutputDriver.cli_command,
            project_file_path,
            output_file_path
        ])

        # check the output
        with open(output_file_path, 'r') as output_file:
            generated_obj = json.load(output_file)
        meta = mock_book_author_publisher()
        for table_name in meta.tables:
            assert table_name in generated_obj
            assert generated_obj[table_name]
