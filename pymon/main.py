"""
CLI Entry point.
"""

import time
import colorama

from .cli import parser
from .monitor import Monitor, Arguments


def main(arguments: Arguments | None):
    """main Entry point of pymon.

    Args:
        arguments (Arguments): Args for watching the codebase.
    """

    colorama.init()

    if not arguments:
        cli_arguments = parser.parse_args()
        arguments = Arguments(
            command=cli_arguments.command,
            patterns=cli_arguments.patterns,
            args=cli_arguments.args,
            watch=cli_arguments.watch,
            debug=cli_arguments.debug,
            clean=cli_arguments.clean,
        )

    monitor = Monitor(arguments)
    monitor.start()

    try:
        while True:
            if not arguments.clean:
                cmd = input()
                if cmd == "rs":
                    monitor.restart_process()
                elif cmd == "stop":
                    monitor.stop()
                    break
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()

    return


if __name__ == "__main__":
    main(arguments=None)
