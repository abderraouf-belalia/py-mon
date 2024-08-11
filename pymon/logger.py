"""
Logging module.
"""

from colorama import Fore, Style


class Logger:
    """Logger class."""

    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW + Style.BRIGHT
    RED = Fore.RED
    CYAN = Fore.CYAN

    @classmethod
    def debug(cls, message: str) -> None:
        """debug Log a debug message

        Args:
            message (str): Debug message.
        """
        print(f"{Logger.CYAN}[pymon] {message}{Style.RESET_ALL}")

    @classmethod
    def info(cls, message: str) -> None:
        """info Log an info message

        Args:
            message (str): Info message.
        """
        print(f"{Logger.GREEN}[pymon] {message}{Style.RESET_ALL}")

    @classmethod
    def warn(cls, message: str) -> None:
        """warn Log a warning message

        Args:
            message (str): Warning message.
        """
        print(f"{Logger.YELLOW}[pymon] {message}{Style.RESET_ALL}")

    @classmethod
    def error(cls, message: str) -> None:
        """error Log an error message

        Args:
            message (str): Error message.
        """
        print(f"{Logger.RED}[pymon] {message}{Style.RESET_ALL}")
