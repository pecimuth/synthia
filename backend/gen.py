import sys

from cli.controller import CommandLineController

if __name__ == '__main__':
    controller = CommandLineController()
    controller.execute(sys.argv[1:])
