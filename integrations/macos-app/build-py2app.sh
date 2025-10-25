#!/bin/bash
# Build Mac app using py2app

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BOLD}Building Mac App with py2app${NC}"
echo

# Check if py2app is installed
if ! python3 -c "import py2app" 2>/dev/null; then
    echo "Installing py2app..."
    pip3 install py2app
fi

cd "$SCRIPT_DIR"

# Clean previous builds
rm -rf build dist

# Build
echo "Building app..."
python3 setup-py2app.py py2app

echo
echo -e "${GREEN}✅ Built: $SCRIPT_DIR/dist/Markdown Fixer.app${NC}"
echo
echo "To install:"
echo "  cp -R \"$SCRIPT_DIR/dist/Markdown Fixer.app\" /Applications/"
