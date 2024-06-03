import os
import subprocess
import traceback

import click

from copilothistoryexporter.utils import SharedValues


@click.command()
@click.option('--port', default=9696, help='Running port')
@click.option('--debug', default=False, help='Debug mode')
@click.argument('project', type=click.Path(exists=True, writable=True), required=False)
def main(port, debug, project):
    project = os.path.abspath(project) if project else os.getcwd()
    SharedValues.change_workspace(project)
    script = os.path.join(os.path.dirname(__file__), "addons", "binding.py")
    launch = "mitmdump" if not debug else "mitmweb"
    shell = f"{launch} -s {script} -p {port}"
    print(f"running on --port {port} --debug {debug} {project}")
    print("running mitm with command: ", shell)

    subprocess.run(shell, shell=True)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.
    :return: 0 for success, 1 for failure.
    :rtype: int
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    sys_main()