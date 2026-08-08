# Scripts

Build and installation scripts for markdown-fixer.

## Scripts

### `build-zipapp.sh`

Builds the self-contained, dependency-free CLI zipapp. No OS gate — the
artifact carries a `/usr/bin/env python3` shebang and runs on any POSIX
system.

```bash
./scripts/build-zipapp.sh            # -> dist/markdown-fixer
./scripts/build-zipapp.sh /tmp/out   # -> /tmp/out/markdown-fixer
```

### `install-all.sh`

Universal installer for **macOS only** — it exits immediately on other
platforms. Installs CLI (via `build-zipapp.sh`), Quick Action, and optionally
the Mac App.

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

Run it from a local clone — it builds the zipapp from `src/`, so it can't be
piped from a bare `curl`:

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --cli
```

On Linux, there's no automated installer: run `build-zipapp.sh` and copy
`dist/markdown-fixer` onto your `PATH` yourself.

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

Creates in `dist/`:

| File | Description |
|------|-------------|
| `markdown_fixer-VERSION-py3-none-any.whl` | Python wheel (`pip install`) |
| `markdown_fixer-VERSION.tar.gz` | Python source distribution |
| `markdown-fixer-VERSION-macos-quick-action.zip` | macOS Finder right-click integration |
| `markdown-fixer-VERSION-jetbrains-plugin.zip` | JetBrains IDE plugin |
| `SHA256SUMS.txt` | Checksums for all artifacts |

**Prerequisites:**

- Python build tools: `pip install build`
- Java 17+ (for JetBrains plugin build)
- Version set in `src/markdown_fixer/__version__.py`

**Creating a GitHub release:**

```bash
# After running build-release.sh:
gh release create vVERSION dist/*.whl dist/*.tar.gz dist/*.zip
```

## See Also

- [Installation Guide](../docs/installation.md)
- [Release Process](../docs/structure.md#distribution)
