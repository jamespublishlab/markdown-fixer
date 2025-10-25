# Claude Code Configuration

This directory contains Claude Code integrations for markdown-fixer.

## Components

### 1. Slash Commands (`commands/`)

Quick commands for common operations.

#### `/fix-markdown`
Fix markdown formatting issues in specific file(s).

**Usage:**
```
/fix-markdown README.md
/fix-markdown docs/*.md
/fix-markdown
```

#### `/fix-all-markdown`
Fix all markdown files in the project.

**Usage:**
```
/fix-all-markdown
```

### 2. Skill (`../skill/`)

A comprehensive Claude Code skill that provides intelligent markdown fixing workflows. The skill enables Claude Code to:

- Automatically detect formatting issues
- Preview changes before applying
- Handle installation and setup
- Work with multiple files intelligently

**Installation:** See [skill/README.md](../skill/README.md)

### 3. Auto-Fix Hook (`hooks/`)

Automatically fixes markdown files after edits.

**How it works:**

- Triggers after each prompt submission
- Detects modified markdown files
- Runs markdown-fixer silently
- Only active if markdown-fixer is installed

**Configuration:** See [hooks/README.md](hooks/README.md)

## Quick Start

### Install markdown-fixer
```bash
# From project root
pip install -e .

# Or with pipx
pipx install -e .
```

### Enable All Features

1. **Slash commands**: Already enabled (in this directory)
2. **Skill**: Available in project (see `skill/` directory)
3. **Auto-fix hook**: Already enabled (see `hooks/` directory)

### Test It

**Try slash commands:**
```
/fix-markdown README.md
```

**Ask naturally:**
```
"Fix the formatting in README.md"
"Check all my markdown files"
```

**Edit and auto-fix:**

1. Edit any .md file
2. Submit a prompt
3. File is automatically fixed

## Usage Comparison

| Method | Best For | Example |
|--------|----------|---------|
| **Slash commands** | Quick, specific operations | `/fix-markdown README.md` |
| **Skill** | Complex workflows, AI-guided | "Fix all docs but show me what changes first" |
| **Auto-fix hook** | Automatic, hands-off | Edit file → auto-fixed on save |
| **Manual** | One-off, custom commands | `markdown-fixer *.md -i` |

## Troubleshooting

### Commands not working?

Check installation:
```bash
which markdown-fixer
markdown-fixer --version
```

If not installed:
```bash
pip install -e .
```

### Hook not running?

Verify it's executable:
```bash
chmod +x .claude/hooks/user-prompt-submit.sh
```

### Want more control?

Disable auto-fix and use slash commands or skill instead:
```bash
mv .claude/hooks/user-prompt-submit.sh .claude/hooks/user-prompt-submit.sh.disabled
```

## Documentation

- [Skill Guide](../skill/README.md) - Detailed skill documentation
- [Hooks Guide](hooks/README.md) - Auto-fix configuration
- [Main README](../README.md) - Project overview

## See Also

For manual usage without Claude Code, see the [main documentation](../README.md).
