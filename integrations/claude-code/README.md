# Claude Code Integration

Claude Code integrations for markdown-fixer: slash commands, skill, and auto-fix hook.

## Installation

### 1. Install markdown-fixer

```bash
pipx install git+https://github.com/jamespublishlab/markdown-fixer.git
# or
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
```

### 2. Install Claude Code Components

Copy the components you want to your Claude Code configuration:

**Slash Commands:**
```bash
# Copy to your global Claude Code commands
cp -r commands/ ~/.claude/commands/
```

**Skill:**
```bash
# Copy to your global Claude Code skills
mkdir -p ~/.claude/skills/
cp skill/markdown-fixer ~/.claude/skills/
```

**Auto-Fix Hook:**
```bash
# Copy hook script
mkdir -p ~/.claude/hooks/
cp hooks/post-markdown-fix.py ~/.claude/hooks/
```

Then add to your `~/.claude/settings.json`:
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

## Components

### Slash Commands (`commands/`)

Quick commands for common operations.

| Command | Description |
|---------|-------------|
| `/fix-markdown [file]` | Fix specific file(s) |
| `/fix-all-markdown` | Fix all markdown files in project |

**Usage:**
```
/fix-markdown README.md
/fix-markdown docs/*.md
/fix-all-markdown
```

### Skill (`skill/`)

AI-guided markdown fixing workflows. The skill enables Claude Code to:

- Automatically detect formatting issues
- Preview changes before applying
- Work with multiple files intelligently

**Usage:**
```
"Fix all markdown files but show me what changes first"
"Which markdown files need fixing?"
```

### Auto-Fix Hook (`hooks/`)

Automatically fixes markdown files after Claude writes or edits them.

**How it works:**

- Triggers after Write/Edit tools complete
- Only processes `.md` files
- Runs markdown-fixer silently
- Only active if markdown-fixer is installed

## Usage Comparison

| Method | Best For | Example |
|--------|----------|---------|
| **Slash commands** | Quick, specific operations | `/fix-markdown README.md` |
| **Skill** | Complex workflows, AI-guided | "Fix all docs but show me changes first" |
| **Auto-fix hook** | Automatic, hands-off | Edit file → auto-fixed |
| **Manual CLI** | One-off, custom commands | `markdown-fixer *.md -i` |

## Troubleshooting

### Commands not working?

Check markdown-fixer installation:
```bash
which markdown-fixer
markdown-fixer --version
```

### Hook not running?

1. Verify the hook script is in place:
   ```bash
   ls -la ~/.claude/hooks/post-markdown-fix.py
   ```

2. Check your settings.json has the hook configured

3. Ensure markdown-fixer is in your PATH

## See Also

- [Main Documentation](../../README.md)
- [Installation Guide](../../docs/installation.md)
- [Usage Guide](../../docs/usage.md)
