#!/usr/bin/env python3
"""
PostToolUse hook to auto-fix markdown files after Write/Edit operations.

This hook runs after Claude writes or edits a file, and automatically
applies markdown-fixer to .md files.
"""

import json
import sys
import subprocess
import shutil


def main():
    # Parse hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Extract file path from tool input
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    # Only process markdown files
    if not file_path.endswith(".md"):
        sys.exit(0)

    # Check if markdown-fixer is installed
    if not shutil.which("markdown-fixer"):
        sys.exit(0)

    # Run markdown-fixer on the file
    try:
        result = subprocess.run(
            ["markdown-fixer", file_path, "--in-place"],
            capture_output=True,
            text=True
        )

        # Optionally provide context back to Claude
        if result.returncode == 0:
            # Silent success - no need to notify Claude
            pass
    except Exception:
        # Don't fail the hook if something goes wrong
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()