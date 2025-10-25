# Documentation Index

Complete guide to all markdown-fixer documentation.

## 📖 Start Here

### New Users

- **[Getting Started Guide](GETTING_STARTED.md)** ⭐ **START HERE**
  - 5-minute quickstart
  - Installation for all platforms
  - Choosing the right integration
  - Common questions and troubleshooting

### Overview

- **[README.md](README.md)** - Main project documentation
  - What markdown-fixer does
  - Feature overview
  - Quick examples
  - All integrations summary

## 🛠️ Installation & Usage

### Command-Line Tool (CLI)

- **[README.md - CLI Section](README.md#command-line)** - Basic CLI usage
- **[Getting Started - CLI](GETTING_STARTED.md#cli-usage)** - Detailed CLI guide
- Built-in help: `markdown-fixer --help`

### macOS Integrations

#### Quick Action (Finder Right-Click)

- **[Quick Action README](integrations/macos-quick-action/README.md)**
  - Installation instructions
  - Usage guide
  - Troubleshooting
- **[Getting Started - Quick Action](GETTING_STARTED.md#macos-quick-action)** - Quick setup

#### Drag-and-Drop App

- **[macOS App README](integrations/macos-app/README.md)**
  - Building the app (Platypus & py2app)
  - Installation
  - Code signing & notarization
- **[Getting Started - macOS App](GETTING_STARTED.md#macos-app)** - Quick setup

### JetBrains IDEs

- **[JetBrains Setup Guide](integrations/jetbrains/SETUP.md)** ⭐ **Detailed**
  - Step-by-step setup for all JetBrains IDEs
  - Import XML configuration
  - Manual setup
  - File Watcher (auto-format on save)
  - Keyboard shortcuts
  - Pre-commit hooks
  - Comprehensive troubleshooting
- **[JetBrains README](integrations/jetbrains/README.md)** - Quick reference
- **[Getting Started - JetBrains](GETTING_STARTED.md#jetbrains-ide)** - Quick setup

### Claude Code Integration

- **[Claude Code README](.claude/README.md)** ⭐ **Comprehensive**
  - All three integration methods
  - Slash commands
  - Skill usage
  - Auto-fix hook
  - Configuration & troubleshooting
- **[Skill Documentation](skill/README.md)** - Claude Code skill
- **[Hooks Documentation](.claude/hooks/README.md)** - Auto-fix hook details
- **[Getting Started - Claude Code](GETTING_STARTED.md#claude-code)** - Quick setup

### Claude Desktop (MCP Server)

- **[MCP Server README](integrations/mcp-server/README.md)** ⭐ **Complete Guide**
  - MCP Protocol overview
  - Installation (automatic & manual)
  - All three tools documented
  - Real-world usage examples
  - Advanced configuration
  - Troubleshooting & debugging
  - Development guide
  - FAQ & security
- **[Getting Started - Claude Desktop](GETTING_STARTED.md#claude-desktop)** - Quick setup

## 🏗️ Project Structure & Development

### Architecture

- **[STRUCTURE.md](STRUCTURE.md)** ⭐ **Architecture Guide**
  - Complete directory layout
  - Design principles
  - Integration points
  - Testing strategy
  - Development workflow
  - Build & release process

### Implementation

- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Original detailed plan
  - Full technical specification
  - All 6 phases documented
  - Extensive code examples
  - Distribution strategies

### Code Documentation

- **Core Module**: `src/markdown_fixer/core.py`
  - `MarkdownFixer` class
  - All formatting rules
  - Well-commented code

- **CLI Module**: `src/markdown_fixer/cli.py`
  - Click-based interface
  - All command-line options

- **Test Suite**: `tests/`
  - `test_core.py` - Core functionality
  - `test_cli.py` - CLI interface
  - 80%+ coverage

## 📦 Distribution & Release

### For End Users

- **PyPI Package**: `pip install markdown-fixer`
- **Homebrew**: `brew tap jamespublishlab/tap && brew install markdown-fixer`
- **Universal Installer**: [scripts/install-all.sh](scripts/install-all.sh)

### For Developers

- **[Development Workflow](STRUCTURE.md#development-workflow)**
  - Setup for contributors
  - Running tests
  - Code quality tools
  - Making changes

- **[Build Process](STRUCTURE.md#distribution)**
  - Release build script
  - Artifact generation
  - Publishing to PyPI

### Release Management

- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[GitHub Actions](.github/workflows/)** - CI/CD pipelines
  - `test.yml` - Automated testing
  - `release.yml` - Automated releases

## 📝 Reference

### What It Fixes

- **[README - What It Fixes](README.md#what-it-fixes)**
  - Blank lines around lists
  - Field metadata to bullets
  - Excessive newlines
  - Smart preservation

### API Reference

**Python Library Usage:**
```python
from markdown_fixer import MarkdownFixer

fixer = MarkdownFixer()
fixed_content = fixer.fix_string(content)
fixer.fix_file("file.md", in_place=True)
```

See `src/markdown_fixer/core.py` for full API documentation.

### Command Reference

```bash
markdown-fixer FILE [OPTIONS]

Options:
  --version              Show version
  --in-place, -i        Modify file in-place
  --dry-run             Preview changes
  --output, -o FILE     Output to specific file
  --verbose, -v         Show detailed output
  --help                Show help
```

## 🆘 Support & Troubleshooting

### Quick Help

- **[Getting Started - Troubleshooting](GETTING_STARTED.md#troubleshooting)**
  - Common issues & solutions
  - Installation problems
  - Permission errors
  - Import errors

### Platform-Specific

- **macOS Quick Action**: [Troubleshooting](integrations/macos-quick-action/README.md#troubleshooting)
- **macOS App**: [Troubleshooting](integrations/macos-app/README.md#troubleshooting)
- **JetBrains**: [Troubleshooting](integrations/jetbrains/SETUP.md#troubleshooting)
- **Claude Code**: [Troubleshooting](.claude/README.md#troubleshooting)
- **MCP Server**: [Troubleshooting](integrations/mcp-server/README.md#troubleshooting)

### Getting Help

- **[GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)** - Report bugs
- **[GitHub Discussions](https://github.com/jamespublishlab/markdown-fixer/discussions)** - Ask questions
- **Email**: james@publishlab.com

## 🤝 Contributing

### How to Contribute

1. Read [STRUCTURE.md - Contributing](STRUCTURE.md#contributing)
2. Fork the repository
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style

- **Formatting**: `black src/ tests/`
- **Linting**: `ruff check src/ tests/`
- **Type Checking**: `mypy src/`
- See [STRUCTURE.md - Code Quality](STRUCTURE.md#code-quality)

## 📄 Legal

- **[LICENSE](LICENSE)** - MIT License
- **Copyright**: © 2025 James

## 🗺️ Quick Navigation

### By User Type

**I'm a developer who wants:**

- Quick CLI tool → [Getting Started - CLI](GETTING_STARTED.md#cli-usage)
- IDE integration → [JetBrains Guide](integrations/jetbrains/SETUP.md)
- Python library → [API Reference](#api-reference)

**I'm a writer who wants:**

- Easiest option → [Getting Started Guide](GETTING_STARTED.md)
- macOS integration → [Quick Action](integrations/macos-quick-action/README.md)
- Drag-and-drop → [macOS App](integrations/macos-app/README.md)

**I use AI assistants:**

- Claude Desktop → [MCP Server](integrations/mcp-server/README.md)
- Claude Code → [Claude Code Guide](.claude/README.md)

**I want to contribute:**

- Start here → [STRUCTURE.md](STRUCTURE.md)
- Architecture → [STRUCTURE.md - Design Principles](STRUCTURE.md#design-principles)
- Development → [STRUCTURE.md - Development Workflow](STRUCTURE.md#development-workflow)

### By Task

**I want to:**

- **Install** → [Getting Started - Installation](GETTING_STARTED.md#step-1-install)
- **Fix a file** → [Getting Started - CLI](GETTING_STARTED.md#step-2-fix-your-first-file)
- **Choose integration** → [Getting Started - Workflow](GETTING_STARTED.md#step-3-choose-your-workflow)
- **Understand what it does** → [README - What It Fixes](README.md#what-it-fixes)
- **See examples** → [README - Features](README.md#features)
- **Report a bug** → [GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)
- **Get help** → [Getting Started - Troubleshooting](GETTING_STARTED.md#troubleshooting)
- **Build from source** → [STRUCTURE.md - Development](STRUCTURE.md#development-workflow)
- **Integrate into my app** → [API Reference](#api-reference)

## 📊 Documentation Stats

- **9 README files** - Platform-specific guides
- **5 major docs** - Overview, getting started, structure, implementation, changelog
- **6 integrations** - Full documentation for each
- **Comprehensive examples** - Every feature demonstrated
- **Troubleshooting guides** - Platform-specific help
- **100% coverage** - Every feature documented

## 🔄 Updates

This documentation is maintained with the project. Last updated: 2025-10-25

To ensure you have the latest documentation:
```bash
git pull origin main
```

Or view online: [GitHub Repository](https://github.com/jamespublishlab/markdown-fixer)

---

**Still can't find what you're looking for?**

Open an issue: [GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)
