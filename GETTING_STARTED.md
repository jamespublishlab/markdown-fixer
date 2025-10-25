# Getting Started with Markdown Fixer

Welcome! This guide will get you up and running with markdown-fixer in under 5 minutes.

## 🚀 5-Minute Quickstart

### Step 1: Install

**Choose the easiest option for you:**

**If you have Python:**
```bash
pip install markdown-fixer
# or
pipx install markdown-fixer
```

**If you're on macOS and use Homebrew:**
```bash
brew tap jamespublishlab/tap
brew install markdown-fixer
```

**If you're installing from this repository:**
```bash
cd markdown-fixer
pip install -e .
```

### Step 2: Fix Your First File

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

- Blank lines around lists ✅
- Field metadata converted to bullets ✅
- Excessive newlines collapsed ✅

### Step 3: Choose Your Workflow

Now that it works, pick the integration that fits your workflow:

| I Want To... | Use This |
|--------------|----------|
| Fix files from the terminal | [CLI](#cli-usage) (you're done!) |
| Right-click files in Finder (macOS) | [Quick Action](#macos-quick-action) |
| Drag-and-drop files (macOS) | [Mac App](#macos-app) |
| Fix in my IDE (JetBrains) | [IDE Integration](#jetbrains-ide) |
| Use with Claude Code | [Claude Code](#claude-code) |
| Use with Claude Desktop | [MCP Server](#claude-desktop) |

---

## 📖 Detailed Installation & Setup

### CLI Usage

You're already set up! Here are common commands:

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

# Specify output file
markdown-fixer input.md --output output.md

# Verbose mode
markdown-fixer file.md -i -v

# Show help
markdown-fixer --help
```

**Pro tip:** Use `-i` for in-place editing, but commit your files to git first for safety!

### macOS Quick Action

**What it does:** Adds "Fix Markdown" to Finder's right-click menu.

**Install:**
```bash
cd integrations/macos-quick-action
# Follow instructions in README.md to create the workflow
# Or run the install script if you have the workflow file
```

**Use:**

1. Right-click any `.md` file in Finder
2. Quick Actions → Fix Markdown
3. Done! File is fixed in-place

**Details:** See [Quick Action Guide](integrations/macos-quick-action/README.md)

### macOS App

**What it does:** Drag-and-drop app for fixing markdown files.

**Install:**
```bash
cd integrations/macos-app
pip install py2app
./build-py2app.sh

# Then drag the .app to /Applications/
```

**Use:**

1. Drag one or more `.md` files onto the app icon
2. Files are fixed in-place
3. Notification shows completion

**Details:** See [Mac App Guide](integrations/macos-app/README.md)

### JetBrains IDE

**What it does:** Adds "Fix Markdown Formatting" to your IDE (PyCharm, IntelliJ, PhpStorm, WebStorm, etc.)

**Quick Setup:**

1. Download [markdown-fixer.xml](integrations/jetbrains/markdown-fixer.xml)
2. Open IDE → **Settings** → **Tools** → **External Tools**
3. Click gear icon → **Import**
4. Select the XML file
5. Done!

**Use:**

1. Right-click any `.md` file
2. External Tools → Fix Markdown Formatting
3. File is fixed in-place

**Add keyboard shortcut (optional):**

- Settings → Keymap
- Search "Fix Markdown"
- Add shortcut (e.g., `Cmd+Shift+F`)

**Details:** See [JetBrains Setup Guide](integrations/jetbrains/README.md)

### Claude Code

**What it does:** Three ways to use markdown-fixer with Claude Code.

**Setup:**
```bash
# Install markdown-fixer (if not already installed)
pip install -e .
```

**Use:**

**1. Slash Commands** (Quick)
```
/fix-markdown README.md
/fix-all-markdown
```

**2. Skill** (AI-Guided)
```
"Fix all markdown files but show me the changes first"
"Which markdown files need fixing?"
```

**3. Auto-Fix Hook** (Automatic)

- Edit any `.md` file
- Submit a prompt
- File is automatically fixed!

**Disable auto-fix:**
```bash
mv .claude/hooks/user-prompt-submit.sh .claude/hooks/user-prompt-submit.sh.disabled
```

**Details:** See [Claude Code Guide](.claude/README.md)

### Claude Desktop

**What it does:** Claude can fix markdown directly in conversations via MCP (Model Context Protocol).

**Quick Install:**
```bash
cd integrations/mcp-server
./install.sh
```

**Restart Claude Desktop** (close and reopen)

**Use:**
Just ask Claude!
```
User: "Fix this markdown:
**Name:** John
**Age:** 30
- Item 1
More text"

Claude: [uses fix_markdown tool]
Here's the fixed version:

- **Name:** John
- **Age:** 30

- Item 1

More text
```

**Available commands:**

- "Fix this markdown: [content]"
- "Fix the file at ~/Documents/README.md"
- "Preview changes to this markdown: [content]"

**Details:** See [MCP Server Guide](integrations/mcp-server/README.md)

---

## ❓ Common Questions

### How do I know if it's installed?

```bash
which markdown-fixer
markdown-fixer --version
```

### What if I get "command not found"?

**Option 1:** Install with pipx (recommended)
```bash
pip install pipx
pipx install markdown-fixer
```

**Option 2:** Add to PATH
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

**Option 3:** Use full path
```bash
python -m markdown_fixer.cli file.md -i
```

### Can I undo changes?

Yes! If you're using git:
```bash
git checkout file.md  # Restore from git
```

Or make a backup first:
```bash
cp file.md file.md.backup
markdown-fixer file.md -i
```

Or use the default behavior (creates `.formatted.md`):
```bash
markdown-fixer file.md  # Creates file.formatted.md
```

### Does it work on Windows?

The CLI works on Windows:
```bash
pip install markdown-fixer
markdown-fixer file.md -i
```

macOS-specific integrations (Quick Action, App) obviously don't work on Windows.

### Can I use this in CI/CD?

Absolutely!

```bash
# In your CI script
pip install markdown-fixer
markdown-fixer --in-place docs/**/*.md
```

Or with pre-commit hooks:
```bash
# .git/hooks/pre-commit
#!/bin/bash
git diff --cached --name-only --diff-filter=ACM | \
  grep '\.md$' | \
  xargs -I {} markdown-fixer {} -i
```

### What exactly does it fix?

1. **Blank lines around lists** - Ensures lists have proper spacing
2. **Field metadata to bullets** - Converts `**Key:** value` patterns to bulleted lists (only if 2+ consecutive)
3. **Excessive newlines** - Collapses 3+ blank lines to 2
4. **Smart preservation** - Never modifies code blocks, blockquotes, etc.

See [README.md](README.md) for detailed examples.

---

## 🆘 Troubleshooting

### Import Error: "No module named 'markdown_fixer'"

**Solution:** Install the package
```bash
pip install -e .  # If in project directory
# or
pip install markdown-fixer  # From PyPI
```

### "Permission denied" when running scripts

**Solution:** Make scripts executable
```bash
chmod +x scripts/install-all.sh
chmod +x integrations/mcp-server/install.sh
```

### Changes don't look right

**Check your input:** Make sure the file is actually markdown (`.md` extension)

**Try dry-run first:**
```bash
markdown-fixer file.md --dry-run
```

**Check for nested code blocks:** Content in ` ```...``` ` is preserved as-is

### Still having issues?

1. Check [Troubleshooting Guide](README.md#troubleshooting)
2. Search [GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)
3. Open a new issue with:
   - Your OS and Python version
   - Input markdown example
   - Expected vs actual output
   - Full error message

---

## 📚 Next Steps

### Learn More

- **[README.md](README.md)** - Complete project documentation
- **[STRUCTURE.md](STRUCTURE.md)** - Project architecture
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

### Advanced Usage

- **[Integration Guides](integrations/)** - Platform-specific setup
- **[Development Guide](STRUCTURE.md#development-workflow)** - Contributing
- **[API Documentation](src/markdown_fixer/core.py)** - Using as a library

### Use as a Python Library

```python
from markdown_fixer import MarkdownFixer

fixer = MarkdownFixer()

# Fix a string
fixed = fixer.fix_string("**Name:** John\n**Age:** 30")
print(fixed)

# Fix a file
fixer.fix_file("README.md", in_place=True)
```

### Get Help

- **Issues:** [GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/jamespublishlab/markdown-fixer/discussions)
- **Email:** james@publishlab.com

---

## 🎉 You're Ready!

You now have markdown-fixer installed and know how to use it. Pick your favorite integration and start fixing markdown!

**Quick links:**

- [CLI Reference](README.md#command-line)
- [All Integrations](README.md#usage)
- [What It Fixes](README.md#what-it-fixes)

Happy formatting! 🔧
