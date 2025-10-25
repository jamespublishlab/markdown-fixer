#!/bin/bash
# Build Mac app using Platypus
# Install Platypus: brew install platypus

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

APP_NAME="Markdown Fixer"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
ICON="$SCRIPT_DIR/icon.icns"

echo -e "${BOLD}Building Mac App: $APP_NAME${NC}"
echo

# Ensure Platypus is installed
if ! command -v platypus &> /dev/null; then
    echo -e "${YELLOW}❌ Platypus not found${NC}"
    echo "Install with: brew install platypus"
    echo "Or download from: https://sveinbjorn.org/platypus"
    exit 1
fi

# Create icon if it doesn't exist (create a basic one)
if [ ! -f "$ICON" ]; then
    echo -e "${YELLOW}⚠ Icon not found, skipping icon...${NC}"
    ICON=""
fi

# Create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Building app with Platypus..."

# Build app with Platypus
if [ -n "$ICON" ]; then
    ICON_FLAG="--app-icon $ICON"
else
    ICON_FLAG=""
fi

platypus \
    --name "$APP_NAME" \
    $ICON_FLAG \
    --author "James" \
    --app-version "1.0.0" \
    --bundle-identifier "com.publishlab.markdown-fixer" \
    --interpreter "/usr/bin/env python3" \
    --interface-type "None" \
    --app-type "Background" \
    --droppable \
    --accepts-files \
    --accepts-text \
    --uniform-type-identifiers "net.daringfireball.markdown|public.plain-text" \
    --suffixes "md|markdown" \
    --background \
    --quit-after-execution \
    "$SCRIPT_DIR/app_wrapper.py" \
    "$BUILD_DIR/$APP_NAME.app"

echo
echo -e "${GREEN}✅ Built: $BUILD_DIR/$APP_NAME.app${NC}"
echo
echo "To install:"
echo "  cp -R \"$BUILD_DIR/$APP_NAME.app\" /Applications/"
echo
echo "To test:"
echo "  Drag a .md file onto the app"
