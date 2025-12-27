# Claude Code Hooks

Auto-fix hook that integrates markdown-fixer with Claude Code.

## Installation

### 1. Install markdown-fixer

```bash
pipx install markdown-fixer
```

### 2. Copy the Hook

```bash
mkdir -p ~/.claude/hooks/
cp post-markdown-fix.py ~/.claude/hooks/
```

### 3. Configure Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.claude/hooks/post-markdown-fix.py\""
          }
        ]
      }
    ]
  }
}
```

## How It Works

### `post-markdown-fix.py`

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

## Customization

Edit the hook script to customize behavior:

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
if file_path.endswith("CHANGELOG.md"):
    sys.exit(0)
```

**Add more file types:**
```python
if not (file_path.endswith(".md") or file_path.endswith(".markdown")):
    sys.exit(0)
```

## Troubleshooting

### Hook Not Running

1. Verify the script exists:
   ```bash
   ls -la ~/.claude/hooks/post-markdown-fix.py
   ```

2. Check settings.json has the hook configured

3. Check markdown-fixer is installed:
   ```bash
   which markdown-fixer
   ```

### Testing Manually

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.md"}}' | python3 ~/.claude/hooks/post-markdown-fix.py
```

### Enable/Disable

To disable: Remove the hooks section from `~/.claude/settings.json`

To re-enable: Add the hooks configuration back

## See Also

- [Claude Code Integration](../README.md) - All Claude Code components
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
