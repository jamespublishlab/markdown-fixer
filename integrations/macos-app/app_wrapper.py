#!/usr/bin/env python3
"""
Drag-and-drop app wrapper for Markdown Fixer.
Uses markdown_fixer package if installed, falls back to embedded version.
"""

import sys
import os
from pathlib import Path

# Try to import from installed package
try:
    from markdown_fixer import MarkdownFixer
except ImportError:
    # Fall back to embedded version
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
    from markdown_fixer import MarkdownFixer


def show_notification(title: str, message: str, sound: str = "Glass"):
    """Show macOS notification."""
    # Escape quotes in message
    message = message.replace('"', '\\"')
    title = title.replace('"', '\\"')

    applescript = f'''
    display notification "{message}" with title "{title}" sound name "{sound}"
    '''
    os.system(f"osascript -e '{applescript}'")


def show_alert(title: str, message: str):
    """Show macOS alert dialog."""
    message = message.replace('"', '\\"')
    title = title.replace('"', '\\"')

    applescript = f'''
    display alert "{title}" message "{message}" as warning
    '''
    os.system(f"osascript -e '{applescript}'")


def main():
    """Process files dropped on the app."""

    # Check if files were provided
    if len(sys.argv) < 2:
        show_alert(
            "No Files Selected",
            "Please drag one or more .md files onto the Markdown Fixer app."
        )
        return

    # Collect markdown files
    markdown_files = []
    for filepath in sys.argv[1:]:
        if os.path.isfile(filepath) and filepath.endswith('.md'):
            markdown_files.append(filepath)

    if not markdown_files:
        show_alert(
            "No Markdown Files",
            "Please select .md files. Other file types are not supported."
        )
        return

    # Process files
    fixer = MarkdownFixer()
    fixed_count = 0
    errors = []

    for filepath in markdown_files:
        try:
            fixer.fix_file(filepath, in_place=True)
            fixed_count += 1
        except Exception as e:
            filename = Path(filepath).name
            errors.append(f"{filename}: {str(e)}")

    # Show results
    if errors:
        error_msg = '\n'.join(errors[:3])  # Show first 3 errors
        if len(errors) > 3:
            error_msg += f"\n\n...and {len(errors) - 3} more errors"

        show_alert(
            "Partial Success",
            f"Fixed {fixed_count} file(s)\n\nErrors:\n{error_msg}"
        )
    elif fixed_count > 0:
        file_word = "file" if fixed_count == 1 else "files"
        show_notification(
            "Markdown Fixer",
            f"Successfully fixed {fixed_count} {file_word}",
            sound="Glass"
        )
    else:
        show_alert(
            "No Files Fixed",
            "No markdown files were processed."
        )


if __name__ == '__main__':
    main()
