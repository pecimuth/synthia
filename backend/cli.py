import argparse

from web.view.project import SaveView

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate random data from a project file.')
    parser.add_argument('project_file', help='path to the project file')
    args = parser.parse_args()

    with open(args.project_file) as project_file:
        save_view = SaveView().loads(project_file.read())
        print(save_view)
