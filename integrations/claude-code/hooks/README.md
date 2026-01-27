# Claude Code Hooks

Auto-fix hook that integrates markdown-fixer with Claude Code.

## Installation

### 1. Install markdown-fixer

```bash
pipx install markdown-fixer
```

### 2. Configure Claude Code

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|mcp__obsidian-mcp-tools__(create|patch|append).*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/markdown-fixer/integrations/claude-code/hooks/pre-markdown-fix.py"
          }
        ]
      }
    ]
  }
}
```

Update the path to match your installation location.

## How It Works

### `pre-markdown-fix.py` (PreToolUse - Recommended)

- **Trigger:** Before Claude uses Write, Edit, or Obsidian MCP tools
- **Purpose:** Clean markdown content before it's written to disk

**What it does:**

1. Receives JSON input about the tool that is about to be used
2. Checks if the file is a markdown file (.md) OR if the content looks like markdown
3. Runs markdown-fixer on the content
4. Returns cleaned content via `updatedInput`

**When it runs:**

- Before Write, Edit, or Obsidian MCP tools execute
- On .md files OR content that looks like markdown (heuristic detection)
- Only if markdown-fixer is installed

### Content Detection

The hook uses heuristic detection to identify markdown content even when the file extension isn't `.md`. It looks for:

- YAML frontmatter (`---`)
- Markdown headers (`# Header`)
- Bold text (`**bold**`)
- Links (`[text](url)`)
- Lists (unordered and ordered)
- Code blocks (triple backticks)
- Blockquotes (`> quote`)
- Wiki-links (`[[link]]`)

If 2 or more indicators are found, the content is treated as markdown.

### Hook Lifecycle

1. **Claude prepares to write/edit** → Hook intercepts
2. **Hook receives JSON** → Contains tool_name, tool_input with content
3. **Hook checks content** → Is it a .md file or looks like markdown?
4. **Hook cleans content** → Runs markdown-fixer
5. **Hook returns** → Returns `updatedInput` with cleaned content
6. **Tool executes** → Writes the already-cleaned content

### Input Format

The hook receives JSON via stdin:

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.md",
    "content": "..."
  }
}
```

### Output Format

If content is modified:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "content": "...cleaned content..."
    }
  }
}
```

## Supported Tools

The hook intercepts:

- **Write** - Creating new files
- **Edit** - Modifying existing files
- **mcp__obsidian-mcp-tools__create_vault_file** - Creating Obsidian notes
- **mcp__obsidian-mcp-tools__patch_vault_file** - Modifying Obsidian notes
- **mcp__obsidian-mcp-tools__append_to_vault_file** - Appending to Obsidian notes

## Customization

Edit the hook script to customize behavior:

**Add verbose output:**

```python
if cleaned and cleaned != content:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": {"content": cleaned},
            "additionalContext": f"Auto-fixed markdown formatting"
        }
    }))
```

**Exclude certain files:**

```python
if "CHANGELOG" in filename:
    sys.exit(0)
```

## Troubleshooting

### Hook Not Running

1. Verify the script exists at the configured path

2. Check settings.json has the hook configured correctly

3. Check markdown-fixer is installed:

   ```bash
   python3 -c "from markdown_fixer import MarkdownFixer; print('OK')"
   ```

### Testing Manually

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.md", "content": "# Header\ntext"}}' | python3 /path/to/pre-markdown-fix.py
```

### Enable/Disable

To disable: Remove the PreToolUse hooks section from `~/.claude/settings.json`

To re-enable: Add the hooks configuration back

## See Also

- [Claude Code Integration](../README.md) - All Claude Code components
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
