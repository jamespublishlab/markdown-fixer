# JetBrains IDE Integration Guide

Add markdown fixing to PhpStorm, PyCharm, IntelliJ IDEA, WebStorm, etc.

## Prerequisites

```bash
pipx install markdown-fixer
```

## Setup Methods

### Method 1: Import XML Configuration (Easiest)

1. **Download** [`external-tool-config.xml`](external-tool-config.xml)

2. **Import to IDE:**
   - **Settings/Preferences** → **Tools** → **External Tools**
   - Click gear icon ⚙️ → **Import...**
   - Select the downloaded XML file
   - Click **OK**

3. **Verify installation:**
   - Right-click any `.md` file
   - You should see **External Tools** → **Fix Markdown Formatting**

4. **(Optional) Add keyboard shortcut:**
   - **Settings** → **Keymap**
   - Search: "Fix Markdown Formatting"
   - Right-click → **Add Keyboard Shortcut**
   - Suggested: `⌘⇧F` (Mac) or `Ctrl+Shift+F` (Windows/Linux)

### Method 2: Manual Setup

1. **Open Settings:** `⌘,` (Mac) or `Ctrl+Alt+S` (Windows/Linux)

2. **Navigate:** **Tools** → **External Tools**

3. **Click** the **+** button

4. **Configure:**
   - **Name:** `Fix Markdown Formatting`
   - **Description:** `Fix common markdown formatting issues`
   - **Program:** `markdown-fixer` (or full path: `/usr/local/bin/markdown-fixer`)
   - **Arguments:** `--in-place "$FilePath$"`
   - **Working directory:** `$ProjectFileDir$`
   - **Advanced Options:**
     - ✅ Synchronize files after execution
     - ✅ Open console for tool output (optional)

5. **Click OK**

## Usage

### Via Context Menu

1. Right-click any `.md` file in the editor or project tree
2. **External Tools** → **Fix Markdown Formatting**
3. File is fixed in-place

### Via Keyboard Shortcut

1. Open a `.md` file
2. Press your assigned shortcut (e.g., `⌘⇧F`)

### Via Find Action

1. Press `⌘⇧A` (Mac) or `Ctrl+Shift+A` (Windows/Linux)
2. Type "Fix Markdown"
3. Select "Fix Markdown Formatting"

## Auto-Format on Save (Optional)

For automatic formatting when you save markdown files:

### Using File Watchers Plugin

1. **Install File Watchers plugin:**
   - **Settings** → **Plugins**
   - Search: "File Watchers"
   - Install and restart IDE

2. **Add File Watcher:**
   - **Settings** → **Tools** → **File Watchers**
   - Click **+** → **Custom**

3. **Configure:**
   - **Name:** `Markdown Fixer`
   - **File type:** `Markdown`
   - **Scope:** `Project Files`
   - **Program:** `markdown-fixer`
   - **Arguments:** `--in-place $FilePath$`
   - **Working directory:** `$ProjectFileDir$`
   - **Trigger:**
     - ✅ On file save
     - ❌ Auto-save
   - **Advanced Options:**
     - ❌ Create output file from stdout
     - ✅ Show console: Never

4. **Click OK**

Now markdown files will be automatically fixed when you save!

## Troubleshooting

### "Cannot run program 'markdown-fixer'"

**Problem:** IDE can't find the command.

**Solutions:**

1. **Check installation:**
   ```bash
   which markdown-fixer
   ```

2. **Use full path:**
   - Change **Program** to full path: `/usr/local/bin/markdown-fixer`
   - Find path with: `which markdown-fixer`

3. **Check PATH in IDE:**
   - IDE may not inherit your shell's PATH
   - **Preferences** → **Appearance & Behavior** → **System Settings** → **HTTP Proxy**
   - Check "Environment variables"

### Nothing happens when I run the tool

1. **Enable console output:**
   - Edit the external tool
   - ✅ Enable "Open console for tool output"

2. **Check file is markdown:**
   - Tool only works on `.md` files

### Changes don't appear immediately

**Solution:** The file should auto-reload. If not:

- **File** → **Synchronize** (or `⌘Y`)

### File Watcher not triggering

1. **Check plugin is enabled:**
   - **Settings** → **Plugins** → Search "File Watchers"

2. **Check scope:**
   - File Watcher settings → Ensure scope includes your files

## Advanced: Pre-commit Hook

Auto-fix markdown before committing:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Fix all staged markdown files
git diff --cached --name-only --diff-filter=ACMR | \
  grep '\.md$' | \
  xargs -I {} markdown-fixer --in-place {}

# Re-add modified files
git diff --cached --name-only --diff-filter=ACMR | \
  grep '\.md$' | \
  xargs git add
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Uninstallation

1. **Settings** → **Tools** → **External Tools**
2. Select "Fix Markdown Formatting"
3. Click **-** (minus) button
4. **OK**

If using File Watcher:

1. **Settings** → **Tools** → **File Watchers**
2. Select "Markdown Fixer"
3. Click **-** button
