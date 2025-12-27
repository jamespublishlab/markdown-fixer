#!/bin/bash
# Build all distribution artifacts for a new release
#
# Output files (all in dist/):
#   markdown_fixer-VERSION-py3-none-any.whl    - Python wheel
#   markdown_fixer-VERSION.tar.gz              - Python source distribution
#   markdown-fixer-VERSION-macos-quick-action.zip - macOS Finder Quick Action
#   markdown-fixer-VERSION-jetbrains-plugin.zip   - JetBrains IDE plugin
#   SHA256SUMS.txt                             - Checksums for all artifacts

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get version from package
VERSION=$(python3 -c "import sys; sys.path.insert(0, 'src'); from markdown_fixer.__version__ import __version__; print(__version__)")

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
mkdir -p dist

# 1. Build Python package
echo
echo -e "${BOLD}[1/5] Building Python package...${NC}"
python3 -m build
echo -e "${GREEN}✓ Python package built${NC}"

# 2. Package Quick Action
echo
echo -e "${BOLD}[2/5] Packaging macOS Quick Action...${NC}"
if [ -d "integrations/macos-quick-action/Fix Markdown.workflow" ]; then
    cd integrations/macos-quick-action
    zip -r -q "../../dist/markdown-fixer-$VERSION-macos-quick-action.zip" "Fix Markdown.workflow"
    cd ../..
    echo -e "${GREEN}✓ Quick Action packaged${NC}"
else
    echo -e "${YELLOW}⚠ Quick Action workflow not found${NC}"
fi

# 3. Build JetBrains plugin
echo
echo -e "${BOLD}[3/5] Building JetBrains plugin...${NC}"
if [ -f "integrations/jetbrains-plugin/gradlew" ]; then
    cd integrations/jetbrains-plugin
    ./gradlew buildPlugin --quiet 2>/dev/null || ./gradlew buildPlugin

    # Find and rename the plugin zip to consistent naming
    PLUGIN_ZIP=$(find build/distributions -name "*.zip" | head -1)
    if [ -n "$PLUGIN_ZIP" ]; then
        cp "$PLUGIN_ZIP" "../../dist/markdown-fixer-$VERSION-jetbrains-plugin.zip"
        echo -e "${GREEN}✓ JetBrains plugin built${NC}"
    else
        echo -e "${YELLOW}⚠ Plugin zip not found after build${NC}"
    fi
    cd ../..
else
    echo -e "${YELLOW}⚠ Skipping JetBrains plugin (gradlew not found)${NC}"
fi

# 4. Build Mac app (optional - requires py2app)
echo
echo -e "${BOLD}[4/5] Building macOS App...${NC}"
if [ -f "integrations/macos-app/build-py2app.sh" ]; then
    echo -e "${YELLOW}⚠ Mac app build requires py2app and additional setup${NC}"
    echo -e "  To build manually: cd integrations/macos-app && ./build-py2app.sh"
else
    echo -e "${YELLOW}⚠ Skipping Mac app (build script not found)${NC}"
fi

# 5. Generate checksums
echo
echo -e "${BOLD}[5/5] Generating checksums...${NC}"
cd dist
shasum -a 256 *.whl *.tar.gz *.zip > SHA256SUMS.txt 2>/dev/null || \
sha256sum *.whl *.tar.gz *.zip > SHA256SUMS.txt 2>/dev/null || \
echo "Checksum tool not available"
cd ..
echo -e "${GREEN}✓ Checksums generated${NC}"

# Summary
echo
echo -e "${BOLD}${GREEN}Build Complete!${NC}"
echo
echo "Artifacts created in dist/:"
echo
ls -lh dist/ 2>/dev/null || ls dist/
echo
echo -e "${BOLD}Next steps:${NC}"
echo "1. Test artifacts on a clean system"
echo "2. Update CHANGELOG.md if needed"
echo "3. Create git tag: git tag -a v$VERSION -m 'Release v$VERSION'"
echo "4. Push tag: git push origin v$VERSION"
echo "5. Create GitHub release:"
echo "   gh release create v$VERSION dist/*.whl dist/*.tar.gz dist/*.zip"
echo "6. Publish to PyPI: twine upload dist/*.whl dist/*.tar.gz"
echo
