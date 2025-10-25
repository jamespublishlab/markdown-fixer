# JetBrains IDE Integration

Fix markdown files directly from PhpStorm, PyCharm, IntelliJ IDEA, WebStorm, and other JetBrains IDEs.

## Quick Start

1. Install the CLI tool:
   ```bash
   pipx install markdown-fixer
   ```

2. Import the external tool:
   - **Settings** → **Tools** → **External Tools** → Import
   - Select `external-tool-config.xml`

3. Use it:
   - Right-click any `.md` file → **External Tools** → **Fix Markdown Formatting**

## Files

- `external-tool-config.xml` - Import this into your IDE
- `SETUP.md` - Detailed setup instructions including File Watchers
- `QUICK-REFERENCE.md` - Quick reference for common tasks

## Features

- **Context Menu**: Right-click to fix markdown files
- **Keyboard Shortcuts**: Assign your own shortcut
- **File Watchers**: Auto-format on save
- **All JetBrains IDEs**: Works in PyCharm, IntelliJ, PhpStorm, WebStorm, etc.

## See Also

- [Detailed Setup Guide](SETUP.md)
- [Quick Reference](QUICK-REFERENCE.md)
