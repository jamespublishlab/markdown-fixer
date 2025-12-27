# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/jamespublishlab/markdown-fixer/releases/tag/v1.0.0
