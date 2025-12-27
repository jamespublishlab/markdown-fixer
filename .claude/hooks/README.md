# Claude Code Hooks

This directory contains hooks that integrate markdown-fixer with Claude Code's workflow.

## Available Hooks

### `post-markdown-fix.py` (Active)

- **Trigger:** After Claude uses Write or Edit tools
- **Purpose:** Automatically fix markdown formatting on .md files

**What it does:**

1. Receives JSON input about the tool that was just used
2. Checks if the file is a markdown file (.md)
3. Runs markdown-fixer on it automatically
4. Operates silently (no output unless errors)

**When it runs:**

- Only after Write or Edit tools complete
- Only on .md files
- Only if markdown-fixer is installed

### `user-prompt-submit.sh.disabled` (Legacy)

The old hook that ran after every user prompt. Disabled in favor of the more targeted PostToolUse approach.

## Configuration

The hook is configured in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/post-markdown-fix.py\""
          }
        ]
      }
    ]
  }
}
```

### Enable/Disable Auto-Fix

**To disable temporarily:**

Remove or comment out the hooks section in `.claude/settings.local.json`.

**To re-enable:**

Add the hooks configuration back to `.claude/settings.local.json`.

### Customize Behavior

Edit `post-markdown-fix.py` to customize:

**Add verbose output:**
```python
if result.returncode == 0:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"Auto-fixed markdown formatting in {file_path}"
        }
    }))
```

**Exclude certain files:**
```python
# Skip CHANGELOG
if file_path.endswith("CHANGELOG.md"):
    sys.exit(0)
```

**Add more file types:**
```python
# Also fix .markdown files
if not (file_path.endswith(".md") or file_path.endswith(".markdown")):
    sys.exit(0)
```

## How It Works

### Hook Lifecycle

1. **Claude writes/edits a file** → Tool completes
2. **Hook receives JSON** → Contains tool_name and file_path
3. **Hook checks file type** → Is it a .md file?
4. **Hook acts** → Runs markdown-fixer if needed
5. **Hook exits** → Code 0 (success)

### Input Format

The hook receives JSON via stdin:

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.md",
    "content": "..."
  },
  "tool_response": {
    "success": true
  }
}
```

### Safety Features

- **Targeted execution**: Only runs on Write/Edit, not every prompt
- **File type filtering**: Only processes .md files
- **Graceful degradation**: Skips if markdown-fixer not installed
- **Error suppression**: Doesn't fail if something goes wrong
- **Silent operation**: No spam in the output
- **Non-blocking**: Doesn't interfere with Claude Code

## Troubleshooting

### Hook Not Running

**Check if hooks are configured:**
```bash
cat .claude/settings.local.json | grep -A 20 hooks
```

**Verify the script exists and is executable:**
```bash
ls -la .claude/hooks/post-markdown-fix.py
```

**Check if markdown-fixer is installed:**
```bash
which markdown-fixer
```

### Testing the Hook Manually

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.md"}}' | python3 .claude/hooks/post-markdown-fix.py
```

### Want to See What It's Doing

Add debug output to the script:
```python
import sys
print(f"Processing: {file_path}", file=sys.stderr)
```

## Comparison: PostToolUse vs UserPromptSubmit

| Aspect | PostToolUse (Current) | UserPromptSubmit (Legacy) |
|--------|----------------------|---------------------------|
| **Trigger** | After Write/Edit tools | After every user prompt |
| **Precision** | Only on file operations | Scans for modified files |
| **Performance** | Faster (targeted) | Slower (git diff on every prompt) |
| **Reliability** | Gets exact file path | May miss files |

## See Also

- [Claude Code README](../README.md) - Overview of all integrations
- [Main README](../../README.md) - Project overview
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)