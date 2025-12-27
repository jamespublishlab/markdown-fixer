# Markdown Fixer

[![PyPI version](https://badge.fury.io/py/markdown-fixer.svg)](https://pypi.org/project/markdown-fixer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/jamespublishlab/markdown-fixer/workflows/Tests/badge.svg)](https://github.com/jamespublishlab/markdown-fixer/actions)

Fix common markdown formatting issues in LLM-generated content with one command.

## 🚀 Quick Start

```bash
# Install
pip install markdown-fixer

# Fix a file
markdown-fixer file.md --in-place

# That's it!
```

**New to markdown-fixer?** See [Getting Started Guide](docs/GETTING_STARTED.md) for a 5-minute tutorial.

**Using Claude Desktop?** → [Simple Setup (no coding!)](docs/CLAUDE_DESKTOP_SIMPLE_SETUP.md)

**Looking for a specific integration?:** [CLI](#command-line) | [macOS](#macos-quick-action) | [JetBrains](#jetbrains-ides-phpstorm-pycharm-intellij-webstorm) | [Claude Code](#claude-code-integration) | [Claude Desktop](#claude-desktop-mcp-server)

## The Problem

LLMs like ChatGPT and Claude consistently produce markdown with formatting issues that break rendering:

**Before:**
```markdown
# Documentation
**Purpose:** Guide for developers
**Status:** Active
This explains the API.
- List item 1
- List item 2
Next section...

Too many blank lines
```

**After:**
```markdown
# Documentation

- **Purpose:** Guide for developers
- **Status:** Active

This explains the API.

- List item 1
- List item 2

Next section...

Too many blank lines
```

## Features

- **Blank lines around lists** - Adds proper spacing
- **Field metadata conversion** - Converts `**Key:** value` pairs to bullets
- **Newline normalization** - Collapses 3+ blank lines to 2
- **Table formatting** - Automatically formats markdown tables with proper alignment and column widths
- **Unicode support** - Handles CJK characters, emoji, and other wide characters in tables
- **Code-block aware** - Never modifies code blocks
- **Multi-platform** - CLI, macOS Quick Action, drag-drop app, JetBrains plugin

## Installation

### Option 1: Homebrew (macOS, Recommended)
```bash
brew tap jamespublishlab/tap
brew install markdown-fixer
```

### Option 2: Universal Installer (macOS)
Installs everything with one command:
```bash
curl -sSL https://raw.githubusercontent.com/jamespublishlab/markdown-fixer/main/scripts/install-all.sh | bash
```

### Option 3: Python Package Only
```bash
pipx install markdown-fixer
```

Or with pip:
```bash
pip install markdown-fixer
```

## Usage

### Command Line

```bash
# Fix a file (creates file.formatted.md)
markdown-fixer document.md

# Fix in-place
markdown-fixer document.md --in-place

# Fix multiple files
markdown-fixer *.md -i

# Preview changes
markdown-fixer document.md --dry-run

# Specify output file
markdown-fixer input.md --output fixed.md

# Show help
markdown-fixer --help
```

### macOS Quick Action

1. Right-click any `.md` file in Finder
2. **Quick Actions** → **Fix Markdown**
3. File is fixed in-place
4. Notification confirms completion

**Setup:** See [Quick Action Guide](integrations/macos-quick-action/README.md)

### Mac Drag-and-Drop App

1. Drag one or more `.md` files onto the **Markdown Fixer** app
2. Files are fixed in-place
3. Notification shows results

**Download:** Get from [Releases](https://github.com/jamespublishlab/markdown-fixer/releases)

### JetBrains IDEs (PhpStorm, PyCharm, IntelliJ, WebStorm)

**Quick Setup:**

1. Download [markdown-fixer.xml](integrations/jetbrains/markdown-fixer.xml)
2. **Settings** → **Tools** → **External Tools** → Import XML
3. Right-click `.md` files → **External Tools** → **Fix Markdown**

**Full Guide:** [JetBrains Setup](integrations/jetbrains/README.md)

### Claude Code Integration

**Three Ways to Use:**

1. **Slash Commands** - Quick operations:
   ```
   /fix-markdown README.md
   /fix-all-markdown
   ```

2. **Skill** - AI-guided workflows:
   ```
   "Fix all docs but show me what changes first"
   "Check which markdown files need fixing"
   ```

3. **Auto-Fix Hook** - Automatic formatting after edits

**Setup:** See [Claude Code Guide](.claude/README.md)

### Claude Desktop (MCP Server)

Integrate directly into Claude Desktop via Model Context Protocol!

**👉 Non-technical user?** → [Simple Setup Guide (no coding required!)](docs/CLAUDE_DESKTOP_SIMPLE_SETUP.md)

**Quick Install (for developers):**
```bash
cd integrations/mcp-server
./install.sh
```

**What it does:**

- Claude can automatically fix markdown you generate
- Preview changes before applying
- Fix files on your local system
- Works seamlessly in conversations and artifacts

**Example:**
```
User: "Fix this markdown: **Name:** John **Age:** 30"
Claude: [uses fix_markdown tool] "Here's the fixed version:
- **Name:** John
- **Age:** 30"
```

**Full Guide:** [MCP Server Setup](integrations/mcp-server/README.md)

## What It Fixes

### 1. Blank Lines Around Lists

**Problem:** Lists run into surrounding text

```markdown
Some text
- Item 1
- Item 2
More text
```

**Fixed:**
```markdown
Some text

- Item 1
- Item 2

More text
```

### 2. Field Metadata to Bullets

**Problem:** `**Key:** value` patterns that should be lists

```markdown
**Author:** James
**Status:** Complete
**Updated:** 2025-10-25
```

**Fixed:**
```markdown
- **Author:** James
- **Status:** Complete
- **Updated:** 2025-10-25
```

**Note:** Single fields are preserved as-is (not converted to bullets).

### 3. Excessive Newlines

**Problem:** 3+ consecutive blank lines

```markdown
Section 1

Section 2
```

**Fixed:**
```markdown
Section 1

Section 2
```

### 4. Table Formatting

**Problem:** Inconsistent column widths and alignment

```markdown
| Name|Age|City|
|---|---|---|
|Alice|25|New York|
|Bob|30|London|
```

**Fixed:**
```markdown
| Name  | Age | City     |
|:------|:----|:---------|
| Alice | 25  | New York |
| Bob   | 30  | London   |
```

**Features:**
- Automatic column width calculation based on content
- Preserves left/center/right alignment markers
- Handles Unicode, CJK characters (中文, 日本語), and emoji (😀, ✅)
- Best-effort handling of malformed tables (missing/extra cells)
- Tables in code blocks are never modified

### 5. Smart Context Awareness

**Never modifies:**

- Code blocks (` ```...``` `)
- Blockquotes
- Headers
- Horizontal rules

## Development

### Setup

```bash
git clone https://github.com/jamespublishlab/markdown-fixer.git
cd markdown-fixer
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
pytest --cov=markdown_fixer --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

### Build Distributions

```bash
chmod +x scripts/build-release.sh
./scripts/build-release.sh
```

## Architecture

```
markdown-fixer/
├── src/markdown_fixer/  # Core Python package
├── integrations/        # Platform-specific wrappers
│   ├── macos-quick-action/
│   ├── macos-app/
│   └── jetbrains/
└── scripts/            # Build and install scripts
```

**Design principle:** Single source of truth for formatting logic, multiple interfaces for different workflows.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file.

## Author

**James** - [PublishLab](https://github.com/jamespublishlab)

## Documentation

- **[Getting Started Guide](docs/GETTING_STARTED.md)** - 5-minute tutorial for new users
- **[Documentation Index](docs/DOCUMENTATION.md)** - Complete guide to all documentation
- **[Project Structure](docs/STRUCTURE.md)** - Architecture and development guide
- **[Implementation Plan](docs/IMPLEMENTATION_PLAN.md)** - Detailed technical specification
- **[Changelog](CHANGELOG.md)** - Version history

### Integration Guides

- **[macOS Quick Action](integrations/macos-quick-action/README.md)** - Finder right-click
- **[macOS App](integrations/macos-app/README.md)** - Drag-and-drop application
- **[JetBrains IDE](integrations/jetbrains-plugin/README.md)** - PyCharm, IntelliJ, etc.
- **[Claude Code](.claude/README.md)** - Slash commands, skill, auto-fix
- **[Claude Desktop MCP Server](integrations/mcp-server/README.md)** - AI integration

## Support

- **Issues:** [GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/jamespublishlab/markdown-fixer/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.
