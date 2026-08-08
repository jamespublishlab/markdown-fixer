# Markdown Fixer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/jamespublishlab/markdown-fixer/workflows/Tests/badge.svg)](https://github.com/jamespublishlab/markdown-fixer/actions)

Fix common markdown formatting issues in LLM-generated content with one command.

## Quick Start

**macOS:**

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --cli     # builds and installs ~/.local/bin/markdown-fixer
markdown-fixer file.md --in-place
```

**Windows, Linux, or by choice on macOS:**

```bash
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
markdown-fixer file.md --in-place
```

`pip install` also gives you `python -m markdown_fixer.mcp_server`; the
zipapp's supported entry for that is `markdown-fixer mcp-server`. On Linux,
build the zipapp yourself with `scripts/build-zipapp.sh` and copy it onto
`PATH` — `install-all.sh` is macOS-only.

**New to markdown-fixer?** See the [Getting Started Guide](docs/getting-started.md).

**Looking for a specific integration?** [CLI](docs/usage.md) | [macOS](docs/integrations.md#macos-quick-action) | [JetBrains](docs/integrations.md#jetbrains-plugin) | [Claude Code](docs/integrations.md#claude-code) | [Claude Desktop](docs/integrations.md#claude-desktop-mcp)

## The Problem

LLMs consistently produce markdown with formatting issues:

**Before:**
```markdown
# Documentation
**Purpose:** Guide for developers
**Status:** Active
This explains the API.
- List item 1
- List item 2
Next section...
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
```

## Features

- **Blank lines around lists** - Adds proper spacing
- **Field metadata conversion** - Converts `**Key:** value` pairs to bullets
- **Newline normalization** - Collapses 3+ blank lines to 2
- **Table formatting** - Auto-formats tables with proper alignment
- **Unicode support** - Handles CJK characters, emoji, and wide characters
- **Code-block aware** - Never modifies code blocks

## What It Fixes

### 1. Blank Lines Around Block Elements

Ensures proper spacing around headings, lists, code blocks, and tables.

### 2. Field Metadata to Bullets

Converts consecutive `**Key:** value` patterns to bulleted lists.

### 3. Excessive Newlines

Collapses 3+ consecutive blank lines to 2.

### 4. Table Formatting

```markdown
| Name  | Age | City     |
|:------|:----|:---------|
| Alice | 25  | New York |
```

Features: automatic column widths, alignment preservation, Unicode support.

### 5. Horizontal Rule Removal

Removes decorative horizontal rules (`---`, `***`, `___`).

### Smart Preservation

Never modifies: code blocks, inline code, blockquotes, headers.

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | 5-minute quickstart tutorial |
| [Installation](docs/installation.md) | All installation methods |
| [Usage](docs/usage.md) | CLI commands and Python library |
| [Integrations](docs/integrations.md) | Platform-specific setup |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |
| [Architecture](docs/structure.md) | Project structure and development |

### Integration Guides

| Platform | Guide |
|----------|-------|
| macOS Quick Action | [integrations/macos-quick-action](integrations/macos-quick-action/README.md) |
| macOS App | [integrations/macos-app](integrations/macos-app/README.md) |
| JetBrains IDEs | [integrations/jetbrains-plugin](integrations/jetbrains-plugin/README.md) |
| Claude Code | [integrations/claude-code](integrations/claude-code/README.md) |
| Claude Desktop | [integrations/mcp-server](integrations/mcp-server/README.md) |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

See [Architecture](docs/structure.md) for development setup.

## License

MIT License - see [LICENSE](LICENSE) file.

## Author

**James** - [PublishLab](https://github.com/jamespublishlab)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
