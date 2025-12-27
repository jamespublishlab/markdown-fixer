# Scripts

Build and installation scripts for markdown-fixer.

## Scripts

### `install-all.sh`

Universal installer for macOS. Installs CLI, Quick Action, and optionally the Mac App.

```bash
# Interactive install (prompts for what to install)
./scripts/install-all.sh

# Install CLI only
./scripts/install-all.sh --cli

# Install everything without prompts
./scripts/install-all.sh --all

# Install specific components
./scripts/install-all.sh --quick-action
./scripts/install-all.sh --app
```

Can also be run directly from GitHub:

```bash
curl -sSL https://raw.githubusercontent.com/jamespublishlab/markdown-fixer/main/scripts/install-all.sh | bash
```

### `install-quick-action.sh`

Installs the macOS Finder Quick Action only.

```bash
./scripts/install-quick-action.sh
```

Copies the Quick Action workflow to `~/Library/Services/`. Requires the workflow to be built first (see `integrations/macos-quick-action/README.md`).

### `build-release.sh`

Builds all distribution artifacts for a new release.

```bash
./scripts/build-release.sh
```

Creates in `dist/release-{version}/`:

- Python wheel (`.whl`)
- Source distribution (`.tar.gz`)
- Quick Action package (`.zip`)
- Mac App package (`.zip`, if build tools available)
- `SHA256SUMS.txt`

**Prerequisites:**

- Python build tools: `pip install build`
- Version set in `src/markdown_fixer/__version__.py`

## See Also

- [Installation Guide](../docs/installation.md)
- [Release Process](../docs/structure.md#distribution)
