# Usage Guide

Complete guide to using markdown-fixer from the command line and as a Python library.

## Command Line Interface

### Basic Commands

```bash
# Fix a file (creates file.formatted.md)
markdown-fixer document.md

# Fix in-place
markdown-fixer document.md --in-place
markdown-fixer document.md -i  # short form

# Preview changes (dry-run)
markdown-fixer document.md --dry-run

# Specify output file
markdown-fixer input.md --output fixed.md
```

### Multiple Files

```bash
# Fix all markdown files in current directory
markdown-fixer *.md -i

# Fix files recursively
markdown-fixer docs/**/*.md -i

# Fix specific files
markdown-fixer README.md CHANGELOG.md -i
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--in-place` | `-i` | Modify files in-place |
| `--dry-run` | | Preview changes without modifying |
| `--output FILE` | `-o` | Write to specific output file |
| `--verbose` | `-v` | Show detailed output |
| `--version` | | Show version number |
| `--help` | `-h` | Show help message |

### Examples

```bash
# Fix with verbose output
markdown-fixer file.md -i -v

# Preview what would change
markdown-fixer file.md --dry-run

# Fix and save to new file
markdown-fixer draft.md -o final.md

# Show help
markdown-fixer --help
```

## Python Library

Use markdown-fixer programmatically in your Python code.

### Basic Usage

```python
from markdown_fixer import MarkdownFixer

fixer = MarkdownFixer()

# Fix a string
fixed = fixer.fix_string("**Name:** John\n**Age:** 30")
print(fixed)
# Output:
# - **Name:** John
# - **Age:** 30
```

### Fix Files

```python
from markdown_fixer import MarkdownFixer

fixer = MarkdownFixer()

# Fix a file in-place
fixer.fix_file("README.md", in_place=True)

# Fix and save to new file
fixer.fix_file("input.md", output_path="output.md")

# Get fixed content without saving
result = fixer.fix_file("document.md")
print(result)
```

### Process Multiple Files

```python
from pathlib import Path
from markdown_fixer import MarkdownFixer

fixer = MarkdownFixer()

# Fix all markdown files in a directory
for md_file in Path("docs").glob("**/*.md"):
    fixer.fix_file(str(md_file), in_place=True)
    print(f"Fixed: {md_file}")
```

### Custom Processing

```python
from markdown_fixer.core import MarkdownFixer

fixer = MarkdownFixer()

# Process content
content = """
# My Document
**Author:** John
**Date:** 2025-01-01
Some text here.
- Item 1
- Item 2
More text.
"""

fixed = fixer.fix_string(content)
print(fixed)
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Fix Markdown
on: [push, pull_request]

jobs:
  fix-markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install git+https://github.com/jamespublishlab/markdown-fixer.git
      - run: markdown-fixer docs/**/*.md --dry-run
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
git diff --cached --name-only --diff-filter=ACM | \
  grep '\.md$' | \
  xargs -I {} markdown-fixer {} -i
```

Or use pre-commit framework:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: markdown-fixer
        name: Fix markdown formatting
        entry: markdown-fixer
        args: [--in-place]
        language: system
        files: \.md$
```

## What Gets Fixed

markdown-fixer automatically corrects these common issues:

### 1. Blank Lines Around Lists

Before:
```markdown
Some text
- Item 1
- Item 2
More text
```

After:
```markdown
Some text

- Item 1
- Item 2

More text
```

### 2. Field Metadata to Bullets

Before:
```markdown
**Author:** John
**Date:** 2025-01-01
**Status:** Active
```

After:
```markdown
- **Author:** John
- **Date:** 2025-01-01
- **Status:** Active
```

### 3. Excessive Newlines

Collapses 3+ blank lines to 2.

### 4. Table Formatting

Before:
```markdown
|Name|Age|City|
|---|---|---|
|Alice|25|NYC|
```

After:
```markdown
| Name  | Age | City |
|:------|:----|:-----|
| Alice | 25  | NYC  |
```

### 5. Block Element Spacing

Ensures proper blank lines around headings, code blocks, lists, and tables.

## What's Preserved

markdown-fixer never modifies:

- Code blocks (` ```...``` `)
- Inline code (`` `code` ``)
- Blockquotes (`> text`)
- Headers formatting

## See Also

- [Installation](installation.md) - Install markdown-fixer
- [Integrations](integrations.md) - IDE and platform integrations
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
