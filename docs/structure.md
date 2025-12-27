# Project Structure

This document describes the organization of the markdown-fixer project.

## Directory Layout

```
markdown-fixer/
├── .claude/                          # Claude Code local settings
│   └── settings.local.json          # Project-specific permissions
│
├── .github/workflows/                # CI/CD pipelines
│   ├── test.yml                      # Test workflow (pytest, coverage)
│   └── release.yml                   # Release workflow (build, publish)
│
├── docs/                             # Documentation
│   ├── README.md                     # Documentation index
│   ├── getting-started.md           # 5-minute quickstart
│   ├── installation.md              # Installation methods
│   ├── usage.md                     # CLI and library usage
│   ├── integrations.md              # Integration overview
│   ├── troubleshooting.md           # Common issues
│   ├── structure.md                 # This file
│   └── claude-desktop-setup.md      # Non-technical setup guide
│
├── integrations/                     # Platform-specific integrations
│   ├── claude-code/                  # Claude Code integration
│   │   ├── commands/                 # Slash commands
│   │   ├── hooks/                    # Auto-fix hooks
│   │   ├── skill/                    # AI skill
│   │   └── README.md                # Claude Code setup guide
│   │
│   ├── jetbrains-plugin/             # Native JetBrains IDE plugin
│   │   ├── src/                      # Kotlin source code
│   │   ├── build.gradle.kts         # Gradle build
│   │   └── README.md                # Plugin documentation
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
├── src/markdown_fixer/               # Core Python package
│   ├── __init__.py                   # Package exports
│   ├── __version__.py                # Version information
│   ├── core.py                       # Formatting logic (MarkdownFixer class)
│   ├── cli.py                        # Command-line interface (Click)
│   └── mcp_server.py                 # MCP server wrapper (delegates to integrations/)
│
├── tests/                            # Test suite
│   ├── fixtures/                     # Test fixtures
│   │   ├── input/                    # Input test files
│   │   └── expected/                 # Expected output files
│   ├── test_core.py                  # Core functionality tests
│   ├── test_cli.py                   # CLI interface tests
│   └── test_mcp_server.py            # MCP server tests
│
├── .gitignore                        # Git ignore rules
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT License
├── README.md                         # Main project documentation
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
4. **IDE Integration** - JetBrains native plugin
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

## Testing Strategy

### Test Coverage

- **Unit Tests**: `tests/test_core.py` - Core formatting logic
- **Integration Tests**: `tests/test_cli.py` - CLI interface
- **MCP Tests**: `tests/test_mcp_server.py` - MCP server
- **Fixtures**: `tests/fixtures/` - Input/expected output pairs
- **Target**: 80%+ coverage

### Running Tests

```bash
pytest                          # Run all tests
pytest --cov                    # With coverage
pytest -v                       # Verbose
pytest tests/test_core.py       # Specific file
```

### Test Organization

```python
# tests/test_core.py
TestListFormatting      # Blank lines around lists
TestFieldMetadata       # Field to bullet conversion
TestNewlineCollapsing   # Excessive newline removal
TestCodeBlockHandling   # Code block preservation
TestTableFormatting     # Table formatting
TestHeadingFormatting   # Heading spacing
TestHorizontalRuleRemoval # HR removal
TestComplexCombinations # Realistic scenarios
TestFileOperations      # File I/O operations
```

## Development Workflow

### Setup

```bash
git clone https://github.com/jamespublishlab/markdown-fixer.git
cd markdown-fixer
pip install -e ".[dev]"
```

### Code Quality

The project uses these tools to maintain code quality:

| Tool | Purpose | Command |
|------|---------|---------|
| **black** | Code formatting | `black src/ tests/` |
| **ruff** | Linting (unused imports, etc.) | `ruff check src/ tests/` |
| **mypy** | Type checking | `mypy src/` |

**Check before committing:**

```bash
# Check formatting (no changes)
black --check src/ tests/

# Check linting
ruff check src/ tests/

# Auto-fix issues
black src/ tests/
ruff check src/ tests/ --fix
```

**Install dev tools:**

```bash
pip install -e ".[dev]"
# or individually:
pip install black ruff mypy pytest
```

CI runs these checks on every PR - run locally first to catch issues early.

### Making Changes

1. Create feature branch
2. Make changes to `src/markdown_fixer/`
3. Add tests to `tests/`
4. Run tests: `pytest`
5. Run linters: `black`, `ruff`, `mypy`
6. Commit and push
7. Create pull request

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

## Documentation

### Core Docs (in `docs/`)

| File | Purpose |
|------|---------|
| README.md | Documentation index |
| getting-started.md | 5-minute quickstart |
| installation.md | All installation methods |
| usage.md | CLI and library reference |
| integrations.md | Integration overview |
| troubleshooting.md | Common issues |
| structure.md | This file |
| claude-desktop-setup.md | Non-technical guide |

### Integration Docs

Each integration has its own README in `integrations/`:

- `integrations/claude-code/README.md` - Claude Code (commands, hooks, skill)
- `integrations/jetbrains-plugin/README.md` - JetBrains
- `integrations/macos-app/README.md` - macOS App
- `integrations/macos-quick-action/README.md` - Quick Action
- `integrations/mcp-server/README.md` - MCP Server

## Contributing

Key points:

- Single source of truth in `core.py`
- Add tests for new features
- Follow existing code style
- Update documentation
- Keep integrations independent

## License

MIT - See [LICENSE](../LICENSE) file.
