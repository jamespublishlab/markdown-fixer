# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-08

### Added
- `markdown-fixer hook claude-code` — the Claude Code PreToolUse hook, now part of the package
- `markdown-fixer mcp-server` — the MCP server, now part of the package
- `markdown-fixer doctor` — reports resolved arming state, config file, and exclusion patterns
- Machine-local config at `$XDG_CONFIG_HOME/markdown-fixer/config.json` (falling back to `~/.config/markdown-fixer/config.json`) with `hook_enabled` and regex `exclude_patterns`
- `MARKDOWN_FIXER_HOOK` env var to arm or force-disable the hook
- `MARKDOWN_FIXER_EXCLUDE_PATTERNS` env var (JSON array) adding to the config's patterns
- Self-contained zipapp build via `scripts/build-zipapp.sh` — no venv required at runtime

### Changed
- **`click` replaced with `argparse`.** The zipapp is stdlib-only and needs no third-party packages at runtime; `wcwidth` remains a dependency of the pip-installed package, where it provides accurate width calculation for wide and CJK characters in tables (`core.py` falls back gracefully when it is absent, which is how the zipapp works without it)
- The Claude Code hook is now installed as a subcommand, so its settings.json entry contains no absolute paths and is identical on every machine
- The MCP server moved from `integrations/mcp-server/server.py` into `markdown_fixer.mcp_server`, removing a `sys.path` manipulation
- The hook is now **opt-in**: unset means off. It must be armed per machine via config or env var
- **New install path (macOS):** `./scripts/install-all.sh --cli` builds the zipapp and installs it to `~/.local/bin/markdown-fixer` with `mdfixer` as a symlink. The installer script is macOS-only (`install-all.sh` exits on non-darwin systems); on Linux, build the zipapp with `scripts/build-zipapp.sh` and copy it to `~/.local/bin` yourself — the artifact carries a `/usr/bin/env python3` shebang and runs on any POSIX system. Windows users continue to use `pip install`. **Users upgrading from a pipx install should run `pipx uninstall markdown-fixer`** to clean up the orphaned venv; the installer only replaces the symlinks to avoid overwriting the venv binary

### Fixed
- **MCP server stability:** JSON-RPC frames that are not dictionaries (e.g. bare `123`) no longer crash the stdin read loop and drop queued requests; the server now returns JSON-RPC error `-32600` (Invalid Request)

### Removed
- **BREAKING:** `MARKDOWN_FIXER_EXCLUDE_PREFIXES`. Replaced by regex `exclude_patterns` in the config file and `MARKDOWN_FIXER_EXCLUDE_PATTERNS`. The old format was colon-separated, which cannot survive the move to regex because regexes contain colons.

  **Migrating:** each old colon-separated prefix becomes one regex. For example, old
  `MARKDOWN_FIXER_EXCLUDE_PREFIXES=/Users/you/vault/Daily/:/Users/you/vault/Weekly/` becomes
  `"exclude_patterns": ["(^|/)(Daily|Weekly)/"]` in the config file — not
  `"exclude_patterns": ["^/Users/you/vault/(Daily|Weekly)/"]`, even though that looks like the
  more literal translation. Anchoring to the absolute path only protects `Write`/`Edit`, which
  send an absolute `file_path`; the Obsidian MCP tools (`mcp__obsidian-mcp-tools__…`) send a
  `filename` relative to the vault root instead (e.g. `Daily/x.md`), which an
  absolute-anchored pattern can never match. Patterns are matched unanchored (`re.search`), so
  the anchor-free `(^|/)(Daily|Weekly)/` form matches both path shapes and is the recommended
  style. See [hooks/README.md](integrations/claude-code/hooks/README.md#3-arm-it) for the full
  explanation
- `integrations/claude-code/hooks/pre-markdown-fix.py` — superseded by the `hook` subcommand
- `integrations/mcp-server/server.py` — its logic moved into `markdown_fixer.mcp_server` (see Changed)
- `integrations/mcp-server/install.sh` — superseded by `./scripts/install-all.sh --cli` plus pointing Claude Desktop at the zipapp's `mcp-server` subcommand (`command: <abs path>/markdown-fixer`, `args: ["mcp-server"]`)

## [1.0.0] - 2025-12-27

Initial release of markdown-fixer.

### Features

- **Blank Lines Around Block Elements**: Adds proper spacing around headings, lists, code blocks, and tables
- **Field Metadata Conversion**: Converts 2+ consecutive `**Key:** value` patterns to bulleted lists
- **Newline Normalization**: Collapses 3+ consecutive blank lines to 2
- **Table Formatting**: Auto-formats tables with proper alignment and column widths
- **Unicode Support**: Handles CJK characters and emoji correctly in tables
- **Horizontal Rule Removal**: Removes decorative `---`, `***`, `___` separators
- **Smart Processing**: Never modifies content inside code blocks or blockquotes

### Integrations

- **CLI**: Command-line tool with `--in-place`, `--dry-run`, `--output`, `--verbose` options
- **macOS Quick Action**: Right-click integration in Finder
- **macOS App**: Drag-and-drop application
- **JetBrains Plugin**: Native plugin for PyCharm, IntelliJ, PhpStorm, WebStorm
- **Claude Code**: Slash commands, AI skill, and auto-fix hook
- **Claude Desktop**: MCP Server integration (Model Context Protocol)

### Installation

- Python package via pip/pipx
- Universal installer script for macOS

### Documentation

- Getting started guide (5-minute quickstart)
- Consolidated docs in `docs/` folder
- Integration guides for each platform
- Developer documentation and contribution guidelines

[1.1.0]: https://github.com/jamespublishlab/markdown-fixer/releases/tag/v1.1.0
[1.0.0]: https://github.com/jamespublishlab/markdown-fixer/releases/tag/v1.0.0
