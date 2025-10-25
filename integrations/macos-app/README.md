# Mac Drag-and-Drop App

Standalone Mac app for fixing markdown files via drag-and-drop.

## Installation

### For End Users

1. Download `Markdown Fixer.app` from releases
2. Drag to `/Applications/`
3. First time: Right-click → Open (to bypass Gatekeeper)

### From Source

**Option A: Platypus (Simpler)**
```bash
brew install platypus
cd integrations/macos-app
chmod +x build-platypus.sh
./build-platypus.sh
```

**Option B: py2app (More Professional)**
```bash
pip install py2app
cd integrations/macos-app
chmod +x build-py2app.sh
./build-py2app.sh
```

## Usage

1. Drag one or more `.md` files onto the app icon
2. Files are fixed in-place
3. Notification shows when complete

## Building for Distribution

### Code Signing (Required for Distribution)

```bash
# Get your Developer ID
security find-identity -v -p codesigning

# Sign the app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  "Markdown Fixer.app"

# Verify
codesign --verify --deep --strict "Markdown Fixer.app"
spctl -a -v "Markdown Fixer.app"
```

### Notarization (Required for macOS 10.15+)

```bash
# Create ZIP
ditto -c -k --keepParent "Markdown Fixer.app" "Markdown-Fixer.zip"

# Submit for notarization
xcrun notarytool submit "Markdown-Fixer.zip" \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --wait

# Staple the ticket
xcrun stapler staple "Markdown Fixer.app"
```

## Requirements

- macOS 10.15 (Catalina) or later
- Python 3.8+ (built-in on modern macOS)

## Troubleshooting

### "App is damaged" error

This means the app isn't signed/notarized. Fix:
```bash
xattr -cr "/Applications/Markdown Fixer.app"
```

### Python errors

The app uses system Python. If issues occur, install markdown-fixer:
```bash
pip3 install markdown-fixer
```
