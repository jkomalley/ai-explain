"""AI-powered command-line tool for instant explanations of code and terminal commands."""

import os
import sys

import click
import pathlib

from pydantic_ai import Agent

__version__ = "0.1.0"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEFAULT_GEMINI_MODEL = "google-gla:gemini-2.0-flash"


def get_piped_input() -> str | None:
    """
    Reads all lines from sys.stdin if data is being piped in.
    Returns the entire piped input as a single string, or None if no pipe.
    """
    if not sys.stdin.isatty():
        # piped input detected, read and return it
        return sys.stdin.read()


def create_agent(instructions, model) -> Agent:
    return Agent(
        DEFAULT_GEMINI_MODEL,
        instructions=instructions,
    )


def generate_explanation(agent, text) -> str:
    result = agent.run_sync(text)

    return result.output


@click.command
@click.argument("text", required=False)
@click.option("-f", "--file", help="Path to a file whose content should be explained.")
def main(text, file) -> None:
    """Explain code, commands, or text using AI."""

    input_text = ""

    if file:
        try:
            input_text = (
                f"FILE NAME: {file} FILE CONTENTS: {pathlib.Path(file).read_text()}"
            )
        except FileNotFoundError:
            click.echo(f"No such file: {file}", err=True)
            sys.exit(1)
    elif text:
        input_text = text
    elif piped_data := get_piped_input():
        input_text = piped_data
    else:
        click.echo(main.get_help(click.get_current_context()))
        sys.exit(1)

    agent = create_agent(
        "You are a helpful file summarizer. Your mission is to take in "
        "text and return a brief summarization.",
        DEFAULT_GEMINI_MODEL,
    )

    if input_text.strip():
        summary = generate_explanation(agent, input_text)

        click.echo(summary.strip())
    else:
        click.echo("Input contains no data.", err=True)
