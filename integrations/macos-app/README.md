# Mac Drag-and-Drop App

Standalone Mac app for fixing markdown files via drag-and-drop.

## Installation

### For End Users

1. Download `Markdown Fixer.app` from releases
2. Drag to `/Applications/`
3. First time: Right-click → Open (to bypass Gatekeeper)

### Building From Source

```bash
# Install py2app in your virtual environment
pip install py2app

# Build the app
cd integrations/macos-app
chmod +x build-py2app.sh
./build-py2app.sh

# The app will be created in dist/Markdown Fixer.app
```

The py2app build method automatically bundles all Python dependencies (including the markdown_fixer module), creating a truly standalone app that doesn't require any system Python packages.

## Usage

1. Drag one or more `.md` files onto the app icon
2. Files are fixed in-place
3. macOS notification shows when complete

## Testing the App

**Method 1: Drag and Drop (Recommended)**
1. Create a test markdown file with formatting issues
2. Drag it onto the app icon in Finder
3. Check for macOS notification confirming the fix
4. Open the file to verify changes were made

**Method 2: Command Line**
```bash
# Open a file with the app (triggers processing)
open -a "dist/Markdown Fixer.app" test-file.md

# Check Console.app for any errors:
log show --predicate 'process == "Markdown Fixer"' --last 5m
```

**Method 3: Direct Executable Test**
```bash
# Run the app's executable directly to see output
"dist/Markdown Fixer.app/Contents/MacOS/Markdown Fixer" test-file.md
```

## Building for Distribution

### Code Signing (Required for Distribution)

```bash
# Get your Developer ID
security find-identity -v -p codesigning

# Sign the app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  "dist/Markdown Fixer.app"

# Verify
codesign --verify --deep --strict "dist/Markdown Fixer.app"
spctl -a -v "dist/Markdown Fixer.app"
```

### Notarization (Required for macOS 10.15+)

```bash
# Create ZIP
ditto -c -k --keepParent "dist/Markdown Fixer.app" "Markdown-Fixer.zip"

# Submit for notarization
xcrun notarytool submit "Markdown-Fixer.zip" \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --wait

# Staple the ticket
xcrun stapler staple "dist/Markdown Fixer.app"
```

## Requirements

- macOS 10.15 (Catalina) or later
- Python 3.8+ with pip (for building only)
- Built app is standalone and doesn't require Python on user systems

## Troubleshooting

### "App is damaged" error

This means the app isn't signed/notarized. Fix:
```bash
xattr -cr "/Applications/Markdown Fixer.app"
```

### Build fails with missing modules

Make sure you're building from a virtual environment that has the markdown-fixer package installed:
```bash
# From the project root
pip install -e .
cd integrations/macos-app
./build-py2app.sh
```

### "pkg_resources is deprecated" warning

This is a harmless warning from setuptools. The app will still work correctly. To suppress it, you can exclude setuptools from the build, but it's included for compatibility.
