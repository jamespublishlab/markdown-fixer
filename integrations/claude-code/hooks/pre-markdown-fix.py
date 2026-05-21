#!/usr/bin/env python3
"""
PreToolUse hook: Clean markdown content before writing.
Intercepts Write, Edit, and Obsidian MCP tools.
"""
import json
import os
import sys


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})

    # Get filename from appropriate field
    filename = (
        tool_input.get("file_path")  # Write, Edit
        or tool_input.get("filename")  # Obsidian MCP
        or ""
    )

    # Honor MARKDOWN_FIXER_EXCLUDE_PREFIXES (colon-separated path prefixes)
    exclude_prefixes = [
        p for p in os.environ.get("MARKDOWN_FIXER_EXCLUDE_PREFIXES", "").split(":") if p
    ]
    if filename and any(filename.startswith(p) for p in exclude_prefixes):
        sys.exit(0)

    content = tool_input.get("content", "")
    if not content:
        sys.exit(0)

    # Only process files with a .md extension. Inferring markdown from content
    # false-positives on code files that use '#' comments (shell, Python, YAML,
    # Dockerfiles, etc.), so gate strictly on the file extension.
    if not filename.lower().endswith(".md"):
        sys.exit(0)

    # Import markdown_fixer
    try:
        from markdown_fixer import MarkdownFixer
    except ImportError:
        # markdown-fixer not installed, pass through
        sys.exit(0)

    # Run fixer
    try:
        fixer = MarkdownFixer()
        cleaned = fixer.fix_string(content)
    except Exception:
        # Any error, pass through unchanged
        sys.exit(0)

    # Only output if changed
    if cleaned and cleaned != content:
        updated_input = dict(tool_input)
        updated_input["content"] = cleaned
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "updatedInput": updated_input,
                    }
                }
            )
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
