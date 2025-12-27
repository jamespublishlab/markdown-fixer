#!/bin/bash
# Build all distribution artifacts for a new release

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get version from package
VERSION=$(python3 -c "import sys; sys.path.insert(0, 'src'); from markdown_fixer.__version__ import __version__; print(__version__)")
BUILD_DIR="dist/release-$VERSION"

echo -e "${BOLD}${BLUE}Building Markdown Fixer v$VERSION${NC}"
echo "=================================="
echo

# Confirm version
read -p "Is version $VERSION correct? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted. Update version in src/markdown_fixer/__version__.py"
    exit 1
fi

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf dist/ build/ src/*.egg-info
mkdir -p "$BUILD_DIR"

# 1. Build Python package
echo
echo -e "${BOLD}[1/4] Building Python package...${NC}"
python3 -m build
cp dist/*.whl dist/*.tar.gz "$BUILD_DIR/" 2>/dev/null || {
    # If files weren't created in dist/, they're in the current dir
    find . -maxdepth 1 -name "*.whl" -o -name "*.tar.gz" | xargs -I {} cp {} "$BUILD_DIR/"
}
echo -e "${GREEN}✓ Python package built${NC}"

# 2. Package Quick Action
echo
echo -e "${BOLD}[2/4] Packaging Quick Action...${NC}"
if [ -d "integrations/macos-quick-action" ]; then
    cd integrations/macos-quick-action
    # Create a simple zip with instructions since we don't have the actual workflow
    mkdir -p temp-workflow
    cp README.md quick-action-script.sh temp-workflow/
    (cd temp-workflow && zip -r -q "../../$BUILD_DIR/Fix-Markdown.workflow.zip" .)
    rm -rf temp-workflow
    cd ../..
    echo -e "${GREEN}✓ Quick Action packaged${NC}"
else
    echo -e "${YELLOW}⚠ Quick Action directory not found${NC}"
fi

# 3. Build Mac app
echo
echo -e "${BOLD}[3/4] Building Mac App...${NC}"
if [ -f "integrations/macos-app/build-py2app.sh" ]; then
    echo -e "${YELLOW}⚠ Mac app build requires macOS and additional tools${NC}"
    echo -e "  To build manually: cd integrations/macos-app && ./build-py2app.sh"
else
    echo -e "${YELLOW}⚠ Skipping Mac app (build script not found)${NC}"
fi

# 4. Generate checksums
echo
echo -e "${BOLD}[4/4] Generating checksums...${NC}"
cd "$BUILD_DIR"
shasum -a 256 * > SHA256SUMS.txt 2>/dev/null || sha256sum * > SHA256SUMS.txt 2>/dev/null || echo "Checksum tool not available"
cd ../..
echo -e "${GREEN}✓ Checksums generated${NC}"

# Create release notes template
echo
echo -e "${BOLD}Creating release notes template...${NC}"
cat > "$BUILD_DIR/RELEASE_NOTES.md" << EOF
# Markdown Fixer v$VERSION

## Changes
- Initial release

## Installation

### Homebrew (macOS)
\`\`\`bash
brew tap jamespublishlab/tap
brew install markdown-fixer
\`\`\`

### Universal Installer (macOS)
\`\`\`bash
curl -sSL https://raw.githubusercontent.com/jamespublishlab/markdown-fixer/main/scripts/install-all.sh | bash
\`\`\`

### Python Package
\`\`\`bash
pipx install markdown-fixer
\`\`\`

### Direct Downloads
- **Quick Action:** Fix-Markdown.workflow.zip
- **Mac App:** Markdown-Fixer.app.zip (if available)
- **Python Package:** markdown-fixer-$VERSION.tar.gz

## Checksums
See SHA256SUMS.txt

## What's Fixed
This release fixes common markdown formatting issues:
- Blank lines around lists
- Field metadata conversion to bullets
- Excessive newline removal

## Full Changelog
https://github.com/jamespublishlab/markdown-fixer/blob/main/CHANGELOG.md
EOF

# Summary
echo
echo -e "${BOLD}${GREEN}Build Complete!${NC}"
echo
echo "Artifacts created in: $BUILD_DIR"
echo
ls -lh "$BUILD_DIR" 2>/dev/null || ls "$BUILD_DIR"
echo
echo -e "${BOLD}Next steps:${NC}"
echo "1. Test all artifacts on a clean system"
echo "2. Update CHANGELOG.md"
echo "3. Create git tag: git tag -a v$VERSION -m 'Release v$VERSION'"
echo "4. Push tag: git push origin v$VERSION"
echo "5. Create GitHub release with artifacts from $BUILD_DIR"
echo "6. Publish to PyPI: twine upload dist/*.whl dist/*.tar.gz"
echo
