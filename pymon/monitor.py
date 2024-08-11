"""
Monitoring module.
"""

from typing import Union, List
from subprocess import Popen
from sys import executable
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

from .logger import Logger as logger


class Arguments:
    """Monitor arguments."""

    # Command to execute, e.g. "poetry run start".
    # If it is a one-word command, "foo", the word is considered
    # as a filename for a python file, "foo.py".
    command: str
    # A list of file extension glob patterns to watch for,
    # e.g. ["*.py"]
    patterns: List[str]
    # A list of additional arguments for our command or python file,
    # e.g. ["-q", "-v"]
    args: List[str]
    # A directory path to watch for changes,
    # e.g. "./package"
    watch: str
    # Toggle debug mode. Shows which file change was detected.
    debug: bool
    # Toggle clean mode.
    clean: bool

    def __init__(
        self,
        command: str,
        patterns: List[str],
        args: List[str],
        watch: str,
        debug: bool,
        clean: bool,
    ) -> None:
        self.command = command
        self.patterns = patterns
        self.args = args
        self.watch = watch
        self.debug = debug
        self.clean = clean


class Monitor:
    """Codebase watcher class."""

    command: str
    patterns: List[str]
    args: List[str]
    watch: str
    debug: bool
    clean: bool

    process: Union[Popen, None]
    event_handler: PatternMatchingEventHandler
    observer: Observer

    def _handle_event(self, event: FileSystemEvent):
        if not self.clean:
            logger.warn("restarting due to changes detected...")

            if self.debug:
                logger.debug(f"{event.event_type} {event.src_path}")

        self.restart_process()

    def __init__(self, arguments: Arguments):
        self.command = arguments.command
        self.patterns = arguments.patterns
        self.args = arguments.args
        self.watch = arguments.watch
        self.debug = arguments.debug
        self.clean = arguments.clean

        self.process = None

        self.event_handler = PatternMatchingEventHandler(patterns=self.patterns)
        self.event_handler.on_modified = self._handle_event
        self.event_handler.on_created = self._handle_event
        self.event_handler.on_deleted = self._handle_event
        self.event_handler.on_moved = self._handle_event

        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.watch, recursive=True)

    def start(self):
        """start Start watching for changes."""
        if not self.clean:
            logger.warn(f"watching path: {self.watch}")
            logger.warn(f"watching patterns: {', '.join(self.patterns)}")
            logger.warn("enter 'rs' to restart or 'stop' to terminate")

        self.observer.start()
        self.start_process()

    def stop(self):
        """stop Stop watching for changes."""
        self.stop_process()
        self.observer.stop()
        self.observer.join()

        if not self.clean:
            logger.error("terminated process")

    def restart_process(self):
        """restart_process Restart process due to detected changes"""
        self.stop_process()
        self.start_process()

    def start_process(self):
        """start_process Start the process."""
        if not self.clean:
            logger.info(f"starting {self.command}")
        command_string = self.command.split(" ")

        # the case where the command is just a py file.
        if len(command_string) == 1:
            command_string = [
                executable,
                self.command + (".py" if not self.command.endswith(".py") else ""),
            ]

        self.process = Popen(
            [
                *command_string,
                *self.args,
            ],
        )

    def stop_process(self):
        """stop_process Stop the process"""
        if self.process:
            self.process.terminate()
            self.process = None
