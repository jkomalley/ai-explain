"""AI-powered command-line tool for instant explanations of code and terminal commands."""

import sys
import click

__version__ = "0.0.0"


def get_piped_input() -> str | None:
    """
    Reads all lines from sys.stdin if data is being piped in.
    Returns the entire piped input as a single string, or None if no pipe.
    """
    if not sys.stdin.isatty():
        # piped input detected
        return sys.stdin.read()


@click.command
@click.argument("text", required=False)
@click.option("-f", "--file", help="Path to a file whose content should be explained.")
def main(text, file) -> None:
    """Explain code, commands, or text using AI."""

    input_text = ""

    if file:
        try:
            with open(file, "r") as f:
                input_text = f.read()
        except FileNotFoundError:
            click.echo(f"Error: File not found: {file}", err=True)
            sys.exit(1)
    elif text:
        input_text = text
    elif piped_data := get_piped_input():
        input_text = piped_data
    else:
        click.echo(main.get_help(click.get_current_context()))
        sys.exit(1)

    if input_text.strip():
        click.echo(f"INPUT: {input_text}")
    else:
        click.echo("Input contains no data.", err=True)
