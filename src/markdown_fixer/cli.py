#!/usr/bin/env python3
"""
Command-line interface for markdown-fixer.
"""

import argparse
import sys
from pathlib import Path

from .__version__ import __version__
from .core import MarkdownFixer

DESCRIPTION = """Fix markdown formatting issues.

Fixes common problems in markdown files:
- Adds blank lines around lists
- Converts field metadata to bulleted lists
- Collapses excessive newlines
"""

EPILOG = """Examples:
  markdown-fixer file.md              Creates file.formatted.md
  markdown-fixer file.md -i           Modifies file.md in-place
  markdown-fixer *.md -i              Fix multiple files
  markdown-fixer file.md --dry-run    Preview changes
"""


def build_parser():
    """Build the argument parser for file-fixing mode."""
    parser = argparse.ArgumentParser(
        prog="markdown-fixer",
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"markdown-fixer, version {__version__}",
    )
    parser.add_argument("files", nargs="+", help="Markdown file(s) to fix")
    parser.add_argument(
        "--in-place",
        "-i",
        action="store_true",
        help="Modify files in-place (default: create .formatted.md)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show changes without writing to file"
    )
    parser.add_argument(
        "--output", "-o", help="Output file path (only valid with single input file)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    return parser


def fix_files(args):
    """Run the fixer over args.files. Returns a process exit code."""
    if args.output and len(args.files) > 1:
        print("Error: --output can only be used with a single input file", file=sys.stderr)
        return 1

    fixer = MarkdownFixer()

    for filepath in args.files:
        path = Path(filepath)

        if not path.exists():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            return 1

        try:
            if args.verbose:
                print(f"Processing: {path}")

            if args.dry_run:
                content = path.read_text(encoding="utf-8")
                formatted = fixer.fix_string(content)

                print(f"\n{'=' * 60}")
                print(f"File: {path}")
                print("=" * 60)
                print(formatted)
                print("=" * 60)

                original_lines = len(content.split("\n"))
                formatted_lines = len(formatted.split("\n"))
                print(f"\nOriginal lines: {original_lines}")
                print(f"Formatted lines: {formatted_lines}")
                print(f"Difference: {formatted_lines - original_lines:+d} lines\n")
            else:
                output_path = fixer.fix_file(
                    str(path), in_place=args.in_place, output_path=args.output or None
                )

                if args.in_place:
                    print(f"Formatted {path} in-place")
                else:
                    print(f"Created formatted file: {output_path}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}", file=sys.stderr)
            if args.verbose:
                import traceback

                traceback.print_exc()
            return 1

    return 0


def main(argv=None):
    """Entry point.

    Always exits via sys.exit() rather than returning a code. zipapp's
    generated __main__.py calls main() WITHOUT wrapping it in sys.exit(), so a
    returned code would be silently discarded by the zipapp while the console
    script honoured it.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(fix_files(args))


if __name__ == "__main__":
    main()
