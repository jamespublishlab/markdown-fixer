# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Every manipulation the fixer performs is now individually config-gated**, with defaults that differ by surface: `blank_lines_around_blocks`, `collapse_blank_runs`, `bullet_field_metadata`, `reflow_tables`, `strip_horizontal_rules`.
- A key's **presence** in the config makes it global; its **absence** leaves each surface to its own default. The **hook** fires automatically on writes Claude makes, so it defaults to whitespace hygiene only — `bullet_field_metadata`, `reflow_tables` and `strip_horizontal_rules` are all off. The **CLI and MCP server** are direct requests to reformat, so they default to running everything, unchanged from before.
- `MARKDOWN_FIXER_FIXES` env var (a JSON object of `{fix_name: bool}`) as the **per-surface** layer. The config file is global by design, which leaves no way to tune one surface; an env var exists only in the process that has it set, so putting it on the hook's command line in `settings.json` tunes the hook alone and cannot bleed into the CLI. Precedence: surface default < config file < env var. A bad entry warns and is skipped; an unparseable value is ignored; neither can disarm the hook.
- `doctor` now prints a per-fix, per-surface table naming the winning layer for each value (`default`, `config` or `env`), so "why did my `---` survive here but vanish there?" is answerable.

### Changed
- **The PreToolUse hook no longer bullets field metadata, reflows tables, or strips horizontal rules by default.** It still normalises blank lines around blocks and collapses blank runs. This is a behaviour change for anyone with the hook armed; set the corresponding keys to `true` to restore the previous behaviour. The library, CLI and MCP server are unaffected.

### Changed
- **Recommended `PreToolUse` matcher narrowed to `^Write$|^mcp__obsidian-mcp-tools__(create|patch|append).*$`.** `Edit` and `Update` were listed and both were dead: the hook reads new content from `tool_input.content`, and `Edit` sends `old_string`/`new_string` instead, so it exits immediately and can never rewrite an edit — while `Update` is not a Claude Code tool at all. Editing an existing markdown file was never auto-fixed; the matcher advertised otherwise. The unanchored form also matched `NotebookEdit`, which would have routed notebook JSON through a markdown fixer.

### Documentation
- Both Claude Code integration READMEs now state the whole-file-writes-only limit explicitly rather than implying edits are covered.

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
- **A non-string entry inside `exclude_patterns` now fails closed** instead of being dropped silently. `{"hook_enabled": true, "exclude_patterns": [["(^|/)Daily/"]]}` — a nested list, the usual typo — previously produced an *armed* hook with zero exclusions and no warning, so every file it saw was rewritten including the ones the config was written to protect. It now marks the config malformed (hook unarmed), and the warning names the offending index. `MARKDOWN_FIXER_EXCLUDE_PATTERNS` keeps the gentler behaviour — a bad entry is warned about and skipped without disarming, since env patterns only add to the config's and cannot shrink them
- **A permission error on the config path no longer escapes `load_config()`.** The `path.exists()` guard sat outside every `try` and swallows only ENOENT/ENOTDIR/EBADF/ELOOP, so an EACCES — an untraversable config directory, or an `XDG_CONFIG_HOME` you cannot read — propagated out of a function documented as never raising, crashing `doctor` with a traceback and no report. It bit only Python ≤ 3.12 (3.13 broadened `exists()` to catch every `OSError`), so it was invisible on a modern dev interpreter while still reaching `/usr/bin/python3` 3.9.6. The pre-check is gone: the file is read directly, `FileNotFoundError` means absent (the normal state under opt-in arming), and any other `OSError` fails closed. Behaviour is now identical on 3.9 and 3.14
- **`markdown-fixer doctor` now names `XDG_CONFIG_HOME`** in its environment-drift note. It decides which config file is read at all, so a hook whose environment differs there is reading a *different config* than the one doctor reported on — previously the note listed only `MARKDOWN_FIXER_HOOK`, `MARKDOWN_FIXER_EXCLUDE_PATTERNS`, and `PATH`

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
