# Markdown Fixer Skill for Claude Code

A Claude Code skill that provides markdown formatting capabilities using the markdown-fixer utility.

## What It Does

This skill enables Claude Code to:

- Fix markdown formatting issues automatically
- Check files for formatting problems
- Batch-process multiple markdown files
- Provide intelligent suggestions for markdown improvements

## Installation

### 1. Install markdown-fixer

```bash
pipx install markdown-fixer
# or
pip install markdown-fixer
```

### 2. Install the Skill Globally

```bash
mkdir -p ~/.claude/skills/
cp markdown-fixer ~/.claude/skills/
```

Or symlink for auto-updates:
```bash
ln -s $(pwd)/markdown-fixer ~/.claude/skills/markdown-fixer
```

## Usage

Once installed, Claude Code can automatically use markdown-fixer when you:

**Ask directly:**

- "Fix the formatting in README.md"
- "Clean up all markdown files"
- "Check if this file needs markdown fixing"

**Get suggestions:**

Claude Code will proactively suggest fixes when it detects:

- Lists without proper spacing
- Field metadata that should be bullets
- Excessive blank lines
- Markdown files with formatting issues

**Examples:**

```
User: "Fix README.md"
Claude: I'll check and fix the markdown formatting...
        [runs markdown-fixer README.md --dry-run]
        Found 3 issues: missing blank lines around 2 lists...
        Should I apply these fixes?

User: "Yes"
Claude: [runs markdown-fixer README.md --in-place]
        Done! Fixed README.md
```

## Features

### Smart Workflows

The skill provides intelligent workflows:

1. **Check first**: Always previews changes with `--dry-run`
2. **Ask permission**: Requests confirmation before modifying files
3. **Batch operations**: Can fix multiple files at once
4. **Error handling**: Gracefully handles missing files or installation issues

### Safe Operations

- Always previews changes before applying
- Recommends committing changes first for bulk operations
- Provides verbose output for debugging
- Preserves code blocks and special content

## Troubleshooting

### Skill Not Found

Make sure:

1. The skill file is in `~/.claude/skills/`
2. The file has the correct name: `markdown-fixer` (no extension)
3. Claude Code has been restarted after installation

### markdown-fixer Not Installed

```bash
pipx install markdown-fixer
```

Verify:
```bash
which markdown-fixer
markdown-fixer --version
```

## See Also

- [Claude Code Integration](../README.md) - All Claude Code components
- [Main Documentation](../../../README.md) - Project overview
