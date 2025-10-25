# Project Structure

This document describes the organization of the markdown-fixer project.

## Directory Layout

```
markdown-fixer/
├── .claude/                          # Claude Code integration
│   ├── commands/                     # Slash commands
│   │   ├── fix-markdown.md          # Fix specific files
│   │   └── fix-all-markdown.md      # Fix all project markdown
│   ├── hooks/                        # Auto-fix hooks
│   │   ├── user-prompt-submit.sh    # Auto-fix on save
│   │   └── README.md                # Hook documentation
│   └── README.md                     # Claude integration overview
│
├── .github/workflows/                # CI/CD pipelines
│   ├── test.yml                      # Test workflow (pytest, coverage)
│   └── release.yml                   # Release workflow (build, publish)
│
├── integrations/                     # Platform-specific integrations
│   ├── jetbrains/                    # JetBrains IDE integration
│   │   ├── markdown-fixer.xml       # Import configuration
│   │   └── README.md                # Complete setup guide
│   │
│   ├── macos-app/                    # macOS drag-and-drop app
│   │   ├── app_wrapper.py           # Python wrapper
│   │   ├── build-py2app.sh          # py2app build script
│   │   ├── setup-py2app.py          # py2app configuration
│   │   └── README.md                # App documentation
│   │
│   ├── macos-quick-action/           # macOS Finder Quick Action
│   │   ├── quick-action-script.sh   # Automator script
│   │   └── README.md                # Installation guide
│   │
│   └── mcp-server/                   # Claude Desktop MCP server
│       ├── server.py                 # MCP server implementation
│       ├── install.sh                # Auto-installer
│       ├── claude_desktop_config.json # Config template
│       ├── requirements.txt          # Server dependencies
│       └── README.md                 # MCP server documentation
│
├── scripts/                          # Build and installation scripts
│   ├── build-release.sh              # Build all release artifacts
│   ├── install-all.sh                # Universal installer (macOS)
│   └── install-quick-action.sh       # Quick Action installer
│
├── skill/                            # Claude Code skill
│   ├── markdown-fixer                # Skill definition (no extension)
│   └── README.md                     # Skill documentation
│
├── src/markdown_fixer/               # Core Python package
│   ├── __init__.py                   # Package exports
│   ├── __version__.py                # Version information
│   ├── core.py                       # Formatting logic (MarkdownFixer class)
│   └── cli.py                        # Command-line interface (Click)
│
├── tests/                            # Test suite
│   ├── fixtures/                     # Test fixtures
│   │   ├── input/                    # Input test files
│   │   └── expected/                 # Expected output files
│   ├── test_core.py                  # Core functionality tests
│   └── test_cli.py                   # CLI interface tests
│
├── .gitignore                        # Git ignore rules
├── CHANGELOG.md                      # Version history
├── IMPLEMENTATION_PLAN.md            # Original detailed implementation plan
├── LICENSE                           # MIT License
├── README.md                         # Main project documentation
├── STRUCTURE.md                      # This file
└── pyproject.toml                    # Python package configuration
```

## Design Principles

### Single Source of Truth

- **Core Logic**: All formatting logic lives in `src/markdown_fixer/core.py`
- **Integrations**: Platform-specific wrappers call the core logic
- **No Duplication**: Each integration reuses the same formatting engine

### Modular Architecture

- **Core Package**: Standalone Python package (pip/pipx installable)
- **Integrations**: Independent, optional platform-specific wrappers
- **Scripts**: Automation for building and installing
- **Tests**: Comprehensive coverage for core and CLI

### Multi-Platform Support
Six usage modes, same logic:

1. **CLI** - Command-line tool (cross-platform)
2. **Quick Action** - macOS Finder right-click
3. **Mac App** - macOS drag-and-drop
4. **IDE Integration** - JetBrains external tool
5. **Claude Code** - AI-assisted workflows
6. **Claude Desktop** - MCP server integration

## Key Files

### Core Implementation

- **`src/markdown_fixer/core.py`**: The heart of the project
  - `MarkdownFixer` class with `fix_string()` and `fix_file()` methods
  - All formatting rules implemented here
  - Well-tested, production-ready

### CLI Interface

- **`src/markdown_fixer/cli.py`**: Command-line interface
  - Built with Click framework
  - Options: `--in-place`, `--dry-run`, `--output`, `--verbose`
  - Entry point: `markdown-fixer` command

### Configuration

- **`pyproject.toml`**: Python package metadata
  - Dependencies, scripts, build configuration
  - Test configuration (pytest, coverage)
  - Code quality tools (black, ruff, mypy)

## Integration Points

### Python Package
```bash
# Install
pip install -e .  # Development
pipx install markdown-fixer  # Production

# Use
from markdown_fixer import MarkdownFixer
fixer = MarkdownFixer()
result = fixer.fix_string(content)
```

### Command Line
```bash
# Installed via pip/pipx
markdown-fixer file.md --in-place
mdfixer *.md -i  # Short alias
```

### macOS Quick Action
```bash
# Install
./scripts/install-quick-action.sh

# Use: Right-click .md file in Finder
```

### JetBrains IDE
```bash
# Import markdown-fixer.xml
# Use: Right-click .md file → External Tools → Fix Markdown
```

### Claude Code
```bash
# Use slash commands
/fix-markdown README.md

# Or ask naturally
"Fix the markdown formatting"

# Auto-fix enabled via hooks
```

### Claude Desktop (MCP)
```bash
# Install
cd integrations/mcp-server
./install.sh

# Use: Ask Claude in Claude Desktop
"Fix this markdown: **Name:** John"
# Claude uses fix_markdown tool automatically
```

## Testing Strategy

### Test Coverage

- **Unit Tests**: `tests/test_core.py` - Core formatting logic
- **Integration Tests**: `tests/test_cli.py` - CLI interface
- **Fixtures**: `tests/fixtures/` - Input/expected output pairs
- **Target**: 80%+ coverage

### Test Organization
```python
# tests/test_core.py
TestListFormatting      # Blank lines around lists
TestFieldMetadata       # Field to bullet conversion
TestNewlineCollapsing   # Excessive newline removal
TestCodeBlockHandling   # Code block preservation
TestComplexCombinations # Realistic scenarios
TestFileOperations      # File I/O operations
```

## Distribution

### Build Artifacts
```bash
./scripts/build-release.sh
# Creates:
# - Python wheel (.whl)
# - Source distribution (.tar.gz)
# - Quick Action (.zip)
# - Mac App (.zip, if tools available)
# - SHA256SUMS.txt
```

### Release Process

1. Update version in `src/markdown_fixer/__version__.py`
2. Update `CHANGELOG.md`
3. Run `./scripts/build-release.sh`
4. Create git tag: `git tag -a v1.0.0`
5. Push tag: `git push origin v1.0.0`
6. GitHub Actions creates release automatically
7. Publish to PyPI (automated)

## Development Workflow

### Setup
```bash
git clone https://github.com/jamespublishlab/markdown-fixer.git
cd markdown-fixer
pip install -e ".[dev]"
```

### Testing
```bash
pytest                          # Run all tests
pytest --cov                    # With coverage
pytest -v                       # Verbose
pytest tests/test_core.py::TestListFormatting  # Specific test
```

### Code Quality
```bash
black src/ tests/               # Format code
ruff check src/ tests/          # Lint
mypy src/                       # Type check
```

### Making Changes

1. Create feature branch
2. Make changes to `src/markdown_fixer/`
3. Add tests to `tests/`
4. Run tests: `pytest`
5. Run linters: `black`, `ruff`, `mypy`
6. Commit and push
7. Create pull request

## Documentation Hierarchy

1. **README.md** - Start here, overview and quick start
2. **IMPLEMENTATION_PLAN.md** - Detailed design and planning
3. **STRUCTURE.md** - This file, project organization
4. **CHANGELOG.md** - Version history
5. **Integration READMEs** - Platform-specific guides
   - `.claude/README.md`
   - `integrations/jetbrains/README.md`
   - `integrations/macos-app/README.md`
   - `integrations/macos-quick-action/README.md`
6. **Skill README** - `skill/README.md` - Claude Code skill

## Contributing

See main [README.md](README.md) for contribution guidelines.

Key points:

- Single source of truth in `core.py`
- Add tests for new features
- Follow existing code style
- Update documentation
- Keep integrations independent

## License

MIT - See [LICENSE](LICENSE) file.
