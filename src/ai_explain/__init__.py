"""AI-powered command-line tool for instant explanations of code and terminal commands."""

import os
import sys

import click
from google import genai
import pathlib

__version__ = "0.1.0"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"


def get_piped_input() -> str | None:
    """
    Reads all lines from sys.stdin if data is being piped in.
    Returns the entire piped input as a single string, or None if no pipe.
    """
    if not sys.stdin.isatty():
        # piped input detected
        return sys.stdin.read()


def generate_explanation(text) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)

    resp = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=text,
        config=genai.types.GenerateContentConfig(
            system_instruction=[
                "You are a helpful file summarizer.",
                "Your mission is to take in text and return a brief summarization.",
            ]
        ),
    )

    return resp.text


@click.command
@click.argument("text", required=False)
@click.option("-f", "--file", help="Path to a file whose content should be explained.")
def main(text, file) -> None:
    """Explain code, commands, or text using AI."""

    input_text = ""

    if file:
        input_text = (
            f"FILE NAME: {file} FILE CONTENTS: {pathlib.Path(file).read_text()}"
        )
    elif text:
        input_text = text
    elif piped_data := get_piped_input():
        input_text = piped_data
    else:
        click.echo(main.get_help(click.get_current_context()))
        sys.exit(1)

    if input_text.strip():
        summary = generate_explanation(input_text)

        click.echo(summary)
    else:
        click.echo("Input contains no data.", err=True)
