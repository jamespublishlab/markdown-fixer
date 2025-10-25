# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-25

### Added
- Initial release
- Core markdown formatting engine
- CLI tool with multiple options (--in-place, --dry-run, --output, --verbose)
- macOS Quick Action integration for Finder
- macOS drag-and-drop application
- JetBrains IDE external tool integration (PhpStorm, PyCharm, IntelliJ, WebStorm)
- Universal installer script for macOS
- Comprehensive test suite with 80%+ coverage
- Support for blank line insertion around lists
- Field metadata to bullet list conversion
- Excessive newline normalization
- Code-block awareness (never modifies code blocks)

### Features
- **Blank Lines Around Lists**: Automatically adds proper spacing before and after lists
- **Field Metadata Conversion**: Converts 2+ consecutive `**Key:** value` patterns to bulleted lists
- **Newline Normalization**: Collapses 3+ consecutive newlines to exactly 2
- **Smart Processing**: Never modifies content inside code blocks
- **Multi-Platform Support**: Available as CLI, macOS Quick Action, macOS App, and JetBrains plugin

### Installation Methods
- Python package via pip/pipx
- Homebrew formula (via tap)
- Universal installer script
- Manual installation for all integrations

### Documentation
- Comprehensive README with usage examples
- Integration guides for macOS Quick Action, macOS App, and JetBrains IDEs
- Build and release automation scripts
- Developer setup and contribution guidelines

[Unreleased]: https://github.com/jamespublishlab/markdown-fixer/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/jamespublishlab/markdown-fixer/releases/tag/v1.0.0
