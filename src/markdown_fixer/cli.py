#!/usr/bin/env python3
"""
Command-line interface for markdown-fixer.
"""

import sys
from pathlib import Path
import click
from .core import MarkdownFixer
from .__version__ import __version__


@click.command()
@click.version_option(version=__version__)
@click.argument("files", nargs=-1, type=click.Path(exists=True), required=True)
@click.option(
    "--in-place", "-i", is_flag=True, help="Modify files in-place (default: create .formatted.md)"
)
@click.option("--dry-run", is_flag=True, help="Show changes without writing to file")
@click.option(
    "--output", "-o", type=click.Path(), help="Output file path (only valid with single input file)"
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def main(files, in_place, dry_run, output, verbose):
    """
    Fix markdown formatting issues.

    Fixes common problems in markdown files:
    - Adds blank lines around lists
    - Converts field metadata to bulleted lists
    - Collapses excessive newlines

    Examples:
        markdown-fixer file.md              # Creates file.formatted.md
        markdown-fixer file.md -i           # Modifies file.md in-place
        markdown-fixer *.md -i              # Fix multiple files
        markdown-fixer file.md --dry-run    # Preview changes
    """
    if output and len(files) > 1:
        click.echo("Error: --output can only be used with a single input file", err=True)
        sys.exit(1)

    fixer = MarkdownFixer()

    for filepath in files:
        try:
            path = Path(filepath)

            if verbose:
                click.echo(f"Processing: {path}")

            if dry_run:
                content = path.read_text(encoding="utf-8")
                formatted = fixer.fix_string(content)

                click.echo(f"\n{'=' * 60}")
                click.echo(f"File: {path}")
                click.echo("=" * 60)
                click.echo(formatted)
                click.echo("=" * 60)

                original_lines = len(content.split("\n"))
                formatted_lines = len(formatted.split("\n"))
                click.echo(f"\nOriginal lines: {original_lines}")
                click.echo(f"Formatted lines: {formatted_lines}")
                click.echo(f"Difference: {formatted_lines - original_lines:+d} lines\n")
            else:
                output_path = fixer.fix_file(
                    str(path), in_place=in_place, output_path=output if output else None
                )

                if in_place:
                    click.echo(f"Formatted {path} in-place")
                else:
                    click.echo(f"Created formatted file: {output_path}")

        except Exception as e:
            click.echo(f"Error processing {filepath}: {e}", err=True)
            if verbose:
                import traceback

                traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
