from cli.controller import CommandLineController

if __name__ == '__main__':
    controller = CommandLineController()
    controller.parse_args()
    controller.parse_project_file()
    controller.generate()
    controller.write_output()
