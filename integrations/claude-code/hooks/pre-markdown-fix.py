#!/usr/bin/env python3
"""
PreToolUse hook: Clean markdown content before writing.
Intercepts Write, Edit, and Obsidian MCP tools.
"""
import json
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

    content = tool_input.get("content", "")
    if not content:
        sys.exit(0)

    # Import markdown_fixer (includes looks_like_markdown utility)
    try:
        from markdown_fixer import MarkdownFixer, looks_like_markdown
    except ImportError:
        # markdown-fixer not installed, pass through
        sys.exit(0)

    # Check if markdown
    is_md_file = filename.lower().endswith(".md")
    is_md_content = looks_like_markdown(content)

    if not (is_md_file or is_md_content):
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
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "updatedInput": {"content": cleaned},
                    }
                }
            )
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
