# Getting Started

Get up and running with markdown-fixer in under 5 minutes.

## Step 1: Install

**Quick install:**

```bash
pip install markdown-fixer
```

**Other options:** See [Installation Guide](installation.md) for Homebrew, pipx, and more.

## Step 2: Fix Your First File

Create a test markdown file with formatting issues:

```bash
cat > test.md << 'EOF'
# My Document
**Author:** John Doe
**Date:** 2025-10-25
This is some text.
- List item 1
- List item 2
More text here.


Too many blank lines.
EOF
```

Fix it:

```bash
markdown-fixer test.md --in-place
```

View the result:

```bash
cat test.md
```

You should see properly formatted markdown with:

- Blank lines around lists
- Field metadata converted to bullets
- Excessive newlines collapsed

## Step 3: Choose Your Workflow

Now that it works, pick the integration that fits how you work:

| I Want To... | Use This |
|--------------|----------|
| Fix files from the terminal | CLI (you're done!) |
| Right-click files in Finder (macOS) | [Quick Action](../integrations/macos-quick-action/README.md) |
| Drag-and-drop files (macOS) | [Mac App](../integrations/macos-app/README.md) |
| Fix in my IDE (JetBrains) | [JetBrains Plugin](../integrations/jetbrains-plugin/README.md) |
| Use with Claude Code | [Claude Code](../.claude/README.md) |
| Use with Claude Desktop | [MCP Server](../integrations/mcp-server/README.md) |

See [Integrations](integrations.md) for a full comparison.

## Quick CLI Reference

```bash
# Preview changes (dry-run)
markdown-fixer file.md --dry-run

# Create a formatted copy (file.formatted.md)
markdown-fixer file.md

# Fix in-place
markdown-fixer file.md --in-place
markdown-fixer file.md -i  # short form

# Fix multiple files
markdown-fixer *.md -i
markdown-fixer docs/**/*.md -i
```

**Full CLI documentation:** [Usage Guide](usage.md)

## Use as a Python Library

```python
from markdown_fixer import MarkdownFixer

fixer = MarkdownFixer()

# Fix a string
fixed = fixer.fix_string("**Name:** John\n**Age:** 30")
print(fixed)

# Fix a file
fixer.fix_file("README.md", in_place=True)
```

**Full API documentation:** [Usage Guide - Python Library](usage.md#python-library)

## Common Questions

### How do I know if it's installed?

```bash
which markdown-fixer
markdown-fixer --version
```

### Can I undo changes?

Yes! If you're using git:

```bash
git checkout file.md
```

Or use the default behavior (creates `.formatted.md`):

```bash
markdown-fixer file.md  # Creates file.formatted.md, review, then rename
```

### What exactly does it fix?

1. **Blank lines around block elements** - Lists, code blocks, headings, tables
2. **Field metadata to bullets** - Converts `**Key:** value` patterns to bulleted lists
3. **Excessive newlines** - Collapses 3+ blank lines to 2
4. **Table formatting** - Auto-formats with proper column widths
5. **Horizontal rules** - Removes decorative `---`, `***`, `___`

See the [main README](../README.md#what-it-fixes) for detailed examples.

## Need Help?

- **Having issues?** See [Troubleshooting](troubleshooting.md)
- **Want more options?** See [Installation](installation.md)
- **Full CLI docs?** See [Usage Guide](usage.md)
- **Platform integrations?** See [Integrations](integrations.md)

## Next Steps

- [Usage Guide](usage.md) - Complete CLI and library reference
- [Integrations](integrations.md) - Set up platform-specific integrations
- [Architecture](structure.md) - Contribute to the project
