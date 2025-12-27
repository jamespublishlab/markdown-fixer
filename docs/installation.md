# Installation

Choose the installation method that works best for your workflow.

## Quick Install

### Homebrew (macOS, Recommended)

```bash
brew tap jamespublishlab/tap
brew install markdown-fixer
```

### pipx (All Platforms)

```bash
pipx install markdown-fixer
```

### pip

```bash
pip install markdown-fixer
```

## Platform-Specific Installation

### macOS Universal Installer

Installs everything (CLI + Quick Action + App) with one command:

```bash
curl -sSL https://raw.githubusercontent.com/jamespublishlab/markdown-fixer/main/scripts/install-all.sh | bash
```

### From Source

```bash
git clone https://github.com/jamespublishlab/markdown-fixer.git
cd markdown-fixer
pip install -e .
```

For development with all tools:

```bash
pip install -e ".[dev]"
```

## Verify Installation

```bash
which markdown-fixer
markdown-fixer --version
```

## Troubleshooting Installation

### "command not found"

**Option 1:** Install with pipx (recommended - handles PATH automatically)

```bash
pip install pipx
pipx install markdown-fixer
```

**Option 2:** Add to PATH

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

**Option 3:** Use Python module directly

```bash
python -m markdown_fixer.cli file.md -i
```

### "Permission denied"

Make install scripts executable:

```bash
chmod +x scripts/install-all.sh
```

### Windows Users

The CLI works on Windows:

```bash
pip install markdown-fixer
markdown-fixer file.md -i
```

Note: macOS-specific integrations (Quick Action, App) are not available on Windows.

## Next Steps

- [Usage Guide](usage.md) - Learn CLI commands and library usage
- [Integrations](integrations.md) - Set up platform-specific integrations
- [Getting Started](getting-started.md) - 5-minute quickstart tutorial
