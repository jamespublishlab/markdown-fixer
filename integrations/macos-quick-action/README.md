# macOS Quick Action for Markdown Fixer

Adds "Fix Markdown" to Finder's right-click menu.

## Installation

### Option 1: Via Installer Script (Recommended)
```bash
./scripts/install-quick-action.sh
```

### Option 2: Manual Installation

1. Double-click `Fix Markdown.workflow`
2. Click "Install" when prompted

### Option 3: Universal Installer
```bash
./scripts/install-all.sh
```

## Usage

1. **Right-click** any `.md` file (or multiple files) in Finder
2. Select **Quick Actions** → **Fix Markdown**
3. Files are fixed in-place
4. Notification shows when complete

## Requirements

- macOS 10.15 (Catalina) or later
- `markdown-fixer` must be installed:
  ```bash
  pipx install markdown-fixer
  ```

## Creating the Workflow Manually

If you need to create the workflow from scratch:

1. Open **Automator** (Applications → Automator)
2. Click **New Document**
3. Select **Quick Action** (or "Service" on older macOS)
4. Configure:
   - "Workflow receives current" → **files or folders**
   - "in" → **Finder**
5. Add **Run Shell Script** action:
   - Set "Shell" to `/bin/bash`
   - Set "Pass input" to **as arguments**
6. Paste the script from `quick-action-script.sh` in this directory
7. Save as **"Fix Markdown"**

## Troubleshooting

### "Markdown Fixer Not Found" error

The Quick Action cannot find the `markdown-fixer` command. Fix:

1. Ensure it's installed: `pipx install markdown-fixer`
2. Check installation: `which markdown-fixer`
3. If using pip instead of pipx, make sure `~/.local/bin` is in PATH

### Quick Action doesn't appear

1. Check if installed: `ls ~/Library/Services/`
2. Restart Finder: `killall Finder`
3. Check System Preferences → Extensions → Finder

### Permission issues

If you get permission errors:
```bash
chmod +x ~/Library/Services/"Fix Markdown.workflow"/Contents/document.wflow
```

## Uninstallation

```bash
rm -rf ~/Library/Services/"Fix Markdown.workflow"
killall Finder
```
