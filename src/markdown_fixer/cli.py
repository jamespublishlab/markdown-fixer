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

RESERVED = frozenset({"hook", "mcp-server", "doctor"})


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

    for filepath in args.files:
        if not Path(filepath).exists():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            return 1

    fixer = MarkdownFixer()

    for filepath in args.files:
        path = Path(filepath)

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


def run_hook(rest):
    """`markdown-fixer hook <host>` -- speak a hook host's protocol on stdin."""
    parser = argparse.ArgumentParser(prog="markdown-fixer hook")
    parser.add_argument(
        "host",
        choices=["claude-code"],
        help="Hook host whose protocol to speak",
    )
    parser.parse_args(rest)

    from .hook import run

    return run()


def run_mcp_server(rest):
    """`markdown-fixer mcp-server` -- JSON-RPC over stdio for Claude Desktop."""
    parser = argparse.ArgumentParser(prog="markdown-fixer mcp-server")
    parser.parse_args(rest)

    from .mcp_server import main as server_main

    server_main()
    return 0


def run_doctor(rest):
    """`markdown-fixer doctor` -- print resolved state."""
    parser = argparse.ArgumentParser(prog="markdown-fixer doctor")
    parser.parse_args(rest)

    from .doctor import report

    return report()


def dispatch(name, rest):
    """Route a reserved first word to its subcommand. Returns an exit code."""
    if name == "hook":
        return run_hook(rest)
    if name == "mcp-server":
        return run_mcp_server(rest)
    if name == "doctor":
        return run_doctor(rest)
    raise AssertionError(f"unhandled reserved word: {name}")


def main(argv=None):
    """Entry point.

    Always exits via sys.exit() rather than returning a code. zipapp's
    generated __main__.py calls main() WITHOUT wrapping it in sys.exit(), so a
    returned code would be silently discarded by the zipapp while the console
    script honoured it.
    """
    if argv is None:
        argv = sys.argv[1:]

    # Reserved words win over filenames: `markdown-fixer hook` never fixes a
    # file called "hook". Use ./hook for that.
    if argv and argv[0] in RESERVED:
        sys.exit(dispatch(argv[0], argv[1:]))

    parser = build_parser()
    args = parser.parse_args(argv)
    sys.exit(fix_files(args))


if __name__ == "__main__":
    main()
