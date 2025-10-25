# Markdown Fixer Skill for Claude Code

A Claude Code skill that provides markdown formatting capabilities using the markdown-fixer utility.

## What It Does

This skill enables Claude Code to:

- Fix markdown formatting issues automatically
- Check files for formatting problems
- Batch-process multiple markdown files
- Provide intelligent suggestions for markdown improvements

## Installation

### Option 1: From This Repository

If you have this repository cloned:

```bash
# The skill file is in the skill/ directory
# Claude Code will auto-detect it when working in this project
```

### Option 2: Install Globally (Recommended)

To make this skill available in ALL Claude Code sessions:

```bash
# Copy to Claude Code's skills directory
# (Location may vary based on your setup)
mkdir -p ~/.claude-code/skills
cp skill/markdown-fixer ~/.claude-code/skills/

# Or symlink it for auto-updates
ln -s $(pwd)/skill/markdown-fixer ~/.claude-code/skills/markdown-fixer
```

### Prerequisites

The markdown-fixer utility must be installed:

```bash
# From this repo
pip install -e .

# Or from PyPI (once published)
pipx install markdown-fixer
```

## Usage

Once the skill is available, Claude Code can automatically use markdown-fixer when you:

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
        ✓ Fixed README.md
```

## Features

### Smart Workflows

The skill provides intelligent workflows:

1. **Check first**: Always previews changes with `--dry-run`
2. **Ask permission**: Requests confirmation before modifying files
3. **Batch operations**: Can fix multiple files at once
4. **Error handling**: Gracefully handles missing files or installation issues

### Auto-Installation

If markdown-fixer isn't installed, Claude Code will:

1. Detect the missing utility
2. Offer to install it
3. Provide installation instructions

### Safe Operations

- Always previews changes before applying
- Recommends committing changes first for bulk operations
- Provides verbose output for debugging
- Preserves code blocks and special content

## Skill Capabilities

Claude Code with this skill can:

✅ Fix single files with preview
✅ Fix multiple files at once
✅ Find and fix all markdown in a project
✅ Show diffs before applying changes
✅ Handle installation and setup
✅ Provide intelligent suggestions
✅ Work with version control (git-aware)

## Configuration

### Auto-Fix on Save (Optional)

See `.claude/hooks/user-prompt-submit.sh` for auto-fix on save configuration.

### Custom Patterns

The skill uses markdown-fixer defaults, but you can customize by:

- Modifying the core logic in `src/markdown_fixer/core.py`
- Adding configuration options to the skill file

## Troubleshooting

### Skill Not Found

Make sure:

1. The skill file is in a location Claude Code can find
2. The file has the correct name: `markdown-fixer` (no extension)
3. Claude Code has been restarted if you just installed it

### markdown-fixer Not Installed

Install it:
```bash
pip install -e .  # If in project dir
# or
pipx install markdown-fixer  # From PyPI
```

Verify:
```bash
which markdown-fixer
markdown-fixer --version
```

### Permission Errors

Ensure the skill file is readable:
```bash
chmod 644 skill/markdown-fixer
```

## Development

To modify the skill:

1. Edit `skill/markdown-fixer`
2. Test by asking Claude Code to use it
3. Iterate on the prompts and commands

The skill file is a plain text prompt that tells Claude Code how to use markdown-fixer effectively.

## Contributing

Improvements to the skill are welcome! Consider:

- Better error handling suggestions
- Additional workflow patterns
- Integration with other tools
- Enhanced user experience

## License

MIT - Same as the parent markdown-fixer project
