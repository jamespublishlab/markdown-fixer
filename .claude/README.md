# Claude Code Configuration

This directory contains custom slash commands for Claude Code.

## Available Commands

### `/fix-markdown`

Fix markdown formatting issues in specific file(s).

**Usage:**
```
/fix-markdown README.md
/fix-markdown docs/*.md
/fix-markdown
```

**What it does:**
- Adds blank lines around lists
- Converts field metadata to bullets
- Normalizes excessive newlines
- Never modifies code blocks

### `/fix-all-markdown`

Fix all markdown files in the project.

**Usage:**
```
/fix-all-markdown
```

**What it does:**
- Finds all .md files in the project
- Asks for confirmation
- Fixes all files in-place

## Setup

These commands require the markdown-fixer utility to be installed:

```bash
# Install from project root
pip install -e .

# Or with pipx
pipx install -e .
```

## Manual Usage

You can also ask Claude Code to run the markdown-fixer directly:

```
"Please run markdown-fixer on README.md"
"Fix the formatting in all my markdown files"
```

Claude Code can use the Bash tool to run any command, so it has full access to markdown-fixer once installed.
