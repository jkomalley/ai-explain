"""AI-powered command-line tool for instant explanations of code and terminal commands."""

import sys

__version__ = "0.0.0"


def get_piped_input() -> str | None:
    """
    Reads all lines from sys.stdin if data is being piped in.
    Returns the entire piped input as a single string, or None if no pipe.
    """
    if not sys.stdin.isatty():
        # piped input detected
        return sys.stdin.read()


def main() -> None:
    data = get_piped_input()

    print(f"Piped data: {data}")
