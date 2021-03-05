import argparse
import json
from argparse import Namespace
from typing import Optional

from cli.reconstruction import ProjectReconstruction
from core.service.generation_procedure.controller import ProcedureController
from core.service.output_driver import PreviewOutputDriver
from core.service.types import json_serialize_default
from web.view.project import SavedProject


class CommandLineController:
    def __init__(self):
        self._args: Optional[Namespace] = None
        self._saved_project: Optional[SavedProject] = None
        self._preview = None

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Generate random data from a project file.')
        parser.add_argument('project_file', help='path to the project file')
        self._args = parser.parse_args()

    def parse_project_file(self):
        with open(self._args.project_file) as project_file:
            project_string = project_file.read()
        reconstruction = ProjectReconstruction(project_string)
        self._saved_project = reconstruction.parse()

    def generate(self):
        preview_driver = PreviewOutputDriver()
        controller = ProcedureController(
            self._saved_project.project,
            self._saved_project.requisition,
            preview_driver
        )
        self._preview = controller.run()

    def write_output(self):
        dumps = json.dumps(
            self._preview.get_dict(),
            indent=2,
            default=json_serialize_default
        )
        print(dumps)
