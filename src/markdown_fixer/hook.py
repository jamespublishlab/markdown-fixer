"""
Claude Code PreToolUse hook.

Reads a PreToolUse payload on stdin and, when the target is an armed,
non-excluded markdown file whose content the fixer would change, writes an
updatedInput carrying the fixed content.

Returns 0 on every path. This hook must never block a write.
"""

import json
import sys

from .config import compile_patterns, is_armed, is_excluded, load_config


def run(stdin=None, stdout=None):
    """Run the hook. Always returns 0."""
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout

    cfg = load_config()
    if not is_armed(cfg):
        return 0

    try:
        payload = json.load(stdin)
    except Exception:  # noqa: BLE001
        # Pathologically deep JSON raises RecursionError, not ValueError/OSError;
        # this must never escape -- a hook failure must never block a write.
        return 0

    if not isinstance(payload, dict):
        return 0

    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0

    # Write/Edit use file_path; the Obsidian MCP tools use filename.
    filename = tool_input.get("file_path") or tool_input.get("filename") or ""
    if not filename or not isinstance(filename, str):
        return 0

    # Gate strictly on the extension. Inferring markdown from content
    # false-positives on '#'-commented code (shell, Python, YAML, Dockerfiles).
    if not filename.lower().endswith(".md"):
        return 0

    if is_excluded(filename, compile_patterns(cfg)):
        return 0

    content = tool_input.get("content", "")
    if not content:
        return 0

    try:
        from .core import MarkdownFixer

        cleaned = MarkdownFixer().fix_string(content)
    except Exception:  # noqa: BLE001
        # Any failure passes the write through untouched.
        return 0

    if cleaned and cleaned != content:
        updated_input = dict(tool_input)
        updated_input["content"] = cleaned
        try:
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "updatedInput": updated_input,
                    }
                },
                stdout,
            )
        except Exception:  # noqa: BLE001
            # e.g. BrokenPipeError if the consumer closed the pipe. This
            # function must never raise -- see module docstring.
            return 0

    return 0
