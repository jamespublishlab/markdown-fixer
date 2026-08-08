# Installation

Choose the installation method that works best for your workflow.

## Quick Install

### macOS: build the zipapp (recommended)

The CLI ships as a self-contained, dependency-free zipapp — no venv, no
`pip`, nothing to break when your Python environment changes later:

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --cli     # builds and installs ~/.local/bin/markdown-fixer
```

This also installs a `mdfixer` alias. Pass `--all` instead of `--cli` to
additionally install the Finder Quick Action and the drag-and-drop Mac App.
`install-all.sh` is macOS-only — it exits immediately on other platforms.

### Linux: build the zipapp by hand

There's no automated installer on Linux, but the artifact itself is
POSIX-capable (it carries a `/usr/bin/env python3` shebang and needs no
venv):

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/build-zipapp.sh                                # -> dist/markdown-fixer
mkdir -p ~/.local/bin
cp dist/markdown-fixer ~/.local/bin/markdown-fixer
chmod +x ~/.local/bin/markdown-fixer
ln -sf ~/.local/bin/markdown-fixer ~/.local/bin/mdfixer   # optional short alias
```

### Windows, or pip on any platform

```bash
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
```

This is also required if you want to invoke the MCP server as
`python -m markdown_fixer.mcp_server`; the zipapp's supported entry for
that is `markdown-fixer mcp-server`.

## Platform-Specific Installation

### macOS Universal Installer

Installs everything (CLI + Quick Action + App) with one command, run from a
local clone:

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --all
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
markdown-fixer doctor       # resolved config, hook arming, exclusion patterns
```

## Troubleshooting Installation

### "command not found"

**Option 1:** Add `~/.local/bin` to PATH (the zipapp installer warns you if
it's missing)

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

**Option 2:** Use the pip-installed Python module directly

```bash
python -m markdown_fixer.cli file.md -i
```

### "Permission denied"

Make install scripts executable:

```bash
chmod +x scripts/install-all.sh
chmod +x scripts/build-zipapp.sh
```

### Windows Users

The CLI works on Windows via pip:

```bash
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
markdown-fixer file.md -i
```

Note: macOS-specific integrations (Quick Action, App, `install-all.sh`) are
not available on Windows.

### Upgrading from an older install

If you installed a previous version through an isolated-environment tool,
remove that old install first — see `CHANGELOG.md` for the exact command.
`install-all.sh` replaces the `~/.local/bin` symlink but will not clean up
whatever it was pointing at.

## Next Steps

- [Usage Guide](usage.md) - Learn CLI commands and library usage
- [Integrations](integrations.md) - Set up platform-specific integrations
- [Getting Started](getting-started.md) - 5-minute quickstart tutorial
