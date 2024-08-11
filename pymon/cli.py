"""
CLI Module
"""

import argparse

parser = argparse.ArgumentParser(
    prog="pymon",
)

parser.add_argument(
    "command",
    type=str,
    help="the command to be executed by pymon",
    metavar="command",
)

parser.add_argument(
    "-p",
    "--patterns",
    type=str,
    help='the file patterns to monitor. use once for each pattern. default "*.py"',
    action="append",
    default=["*.py"],
    metavar="patterns",
)

parser.add_argument(
    "-w",
    "--watch",
    type=str,
    help='the directory to monitor for changes. default "."',
    action="store",
    default=".",
    metavar="path",
)

parser.add_argument(
    "-a",
    "--args",
    type=str,
    help="arguments to pass on to the execution script. use once for each argument.",
    action="append",
    default=[],
    metavar="command",
)

parser.add_argument(
    "-d",
    "--debug",
    help="logs detected file changes to the terminal",
    action="store_true",
)

parser.add_argument(
    "-c",
    "--clean",
    help="runs pymon in clean mode (no logs, no commands)",
    action="store_true",
)
