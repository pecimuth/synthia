import argparse
import json
from argparse import Namespace
from inspect import signature
from typing import Optional, Type, List

from cli.reconstruction import ProjectReconstruction
from core.service.data_source.database_common import DatabaseConnectionManager
from core.service.generation_procedure.controller import ProcedureController
from core.service.output_driver import OutputDriver
from core.service.output_driver.database import DatabaseOutputDriver
from core.service.output_driver.file_driver.base import FileOutputDriver
from web.view.project import SavedProject


class CommandLineController:
    """Controller for the CLI."""

    def __init__(self):
        self._args: Optional[Namespace] = None
        self._saved_project: Optional[SavedProject] = None
        self._driver: Optional[OutputDriver] = None
        self._conn_manager = DatabaseConnectionManager()

    def execute(self, args: List[str]):
        """Parse arguments, generate the data and write to the output resource."""
        self._parse_args(args)
        self._parse_project_file()
        self._generate()
        self._maybe_write_output()
        self._conn_manager.clean_up()

    def _parse_args(self, args: List[str]):
        """Assemble argument parser and parse the command arguments."""
        parser = argparse.ArgumentParser(description='Generate random data from a project file.')
        subparsers = parser.add_subparsers(required=True)
        self._assemble_insert_command(subparsers)
        for file_driver in FileOutputDriver.__subclasses__():
            self._assemble_file_command(subparsers, file_driver)
        self._args = parser.parse_args(args)

    def _assemble_insert_command(self, subparsers):
        """Assemble an INSERT command for the parser."""
        insert_parser = subparsers.add_parser(DatabaseOutputDriver.cli_command)
        self._add_project_argument(insert_parser)
        insert_parser.add_argument('url', help='SQLAlchemy database connection string')
        insert_parser.set_defaults(
            make_driver=lambda args: setattr(self,
                                             '_driver',
                                             DatabaseOutputDriver(args.url, self._conn_manager))
        )

    def _assemble_file_command(self, subparsers, file_driver: Type[FileOutputDriver]):
        """Assemble a command for an output file driver."""
        file_parser = subparsers.add_parser(file_driver.cli_command)
        self._add_project_argument(file_parser)
        sig = signature(file_driver.dump)
        output_bytes = sig.return_annotation == bytes
        file_parser.add_argument(
            'output',
            help='path to the output file',
            type=argparse.FileType('wb' if output_bytes else 'w'),
            nargs=1 if output_bytes else '?'
        )
        file_parser.set_defaults(
            make_driver=lambda args: setattr(self, '_driver', file_driver())
        )

    @staticmethod
    def _add_project_argument(parser: argparse.ArgumentParser):
        """Add positional argument to the parser, taking
        path to the project file."""
        parser.add_argument('project',
                            help='path to the project file',
                            type=argparse.FileType('r'))

    def _parse_project_file(self):
        """Read the contents of the project file, close the file
        and reconstruct the project entities.
        """
        project = json.loads(self._args.project.read())
        self._args.project.close()
        reconstruction = ProjectReconstruction(project)
        self._saved_project = reconstruction.parse()

    def _generate(self):
        """Create the driver, controller and run the generation."""
        self._args.make_driver(self._args)
        controller = ProcedureController(
            self._saved_project.project,
            self._saved_project.requisition,
            self._driver
        )
        controller.run()

    def _maybe_write_output(self):
        """Depending on the type of the output driver,
        write to the output file or standard output.
        """
        if not isinstance(self._driver, FileOutputDriver):
            return
        dump = self._driver.dump()
        if not self._args.output:
            print(dump)
        elif isinstance(self._args.output, list):
            self._args.output[0].write(dump)
            self._args.output[0].close()
        else:
            self._args.output.write(dump)
            self._args.output.close()
