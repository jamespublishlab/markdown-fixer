#!/bin/bash
# Markdown Fixer - Universal Installer
# Installs CLI, Quick Action, and optionally the Mac App
#
# Usage:
#   ./install-all.sh          # Interactive install
#   ./install-all.sh --cli    # CLI only
#   ./install-all.sh --all    # Everything without prompts

set -e

# Colors
BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERSION="1.0.0"
REPO="jamespublishlab/markdown-fixer"
GITHUB_URL="https://github.com/$REPO"

# Parse arguments
INSTALL_CLI=false
INSTALL_QUICK_ACTION=false
INSTALL_APP=false
INTERACTIVE=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --cli)
            INSTALL_CLI=true
            INTERACTIVE=false
            ;;
        --quick-action)
            INSTALL_QUICK_ACTION=true
            INTERACTIVE=false
            ;;
        --app)
            INSTALL_APP=true
            INTERACTIVE=false
            ;;
        --all)
            INSTALL_CLI=true
            INSTALL_QUICK_ACTION=true
            INSTALL_APP=true
            INTERACTIVE=false
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--cli] [--quick-action] [--app] [--all]"
            exit 1
            ;;
    esac
    shift
done

# Header
clear
echo -e "${BOLD}${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║    Markdown Fixer Installer v$VERSION    ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo "Fix common markdown formatting issues"
echo "Repository: $GITHUB_URL"
echo

# Check OS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}✗ This installer is for macOS only${NC}"
    echo "For other platforms, use: pip install git+https://github.com/jamespublishlab/markdown-fixer.git"
    exit 1
fi

# Check Python
echo -e "${BLUE}Checking requirements...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3.8 or later from python.org"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check for pipx (recommended) or pip
if command -v pipx &> /dev/null; then
    INSTALLER="pipx"
    echo -e "${GREEN}✓ pipx found (recommended)${NC}"
elif command -v pip3 &> /dev/null; then
    INSTALLER="pip3"
    echo -e "${YELLOW}⚠ Using pip3 (pipx recommended)${NC}"
    echo "  Consider installing pipx: brew install pipx"
else
    echo -e "${RED}✗ Neither pipx nor pip found${NC}"
    exit 1
fi

echo

# Interactive mode
if $INTERACTIVE; then
    echo -e "${BOLD}What would you like to install?${NC}"
    echo

    read -p "Install CLI tool? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        INSTALL_CLI=true
    fi

    read -p "Install Quick Action (Finder right-click)? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        INSTALL_QUICK_ACTION=true
    fi

    read -p "Install Mac App (drag-and-drop)? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        INSTALL_APP=true
    fi

    echo
fi

# 1. Install CLI tool
if $INSTALL_CLI; then
    echo -e "${BOLD}${BLUE}[1/3] Installing CLI tool...${NC}"

    if $INSTALLER install markdown-fixer; then
        echo -e "${GREEN}✓ CLI installed successfully${NC}"
        echo -e "  Command: ${BOLD}markdown-fixer${NC}"

        # Verify installation
        if command -v markdown-fixer &> /dev/null; then
            VERSION_OUTPUT=$(markdown-fixer --version 2>&1 || echo "version check failed")
            echo -e "  ${VERSION_OUTPUT}"
        fi
    else
        echo -e "${RED}✗ Failed to install CLI${NC}"
        exit 1
    fi
    echo
fi

# 2. Install Quick Action
if $INSTALL_QUICK_ACTION; then
    echo -e "${BOLD}${BLUE}[2/3] Installing Quick Action...${NC}"

    WORKFLOW_DIR="$HOME/Library/Services"
    WORKFLOW_NAME="Fix Markdown.workflow"

    mkdir -p "$WORKFLOW_DIR"

    # Check if local workflow exists
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

    if [ -d "$PROJECT_ROOT/integrations/macos-quick-action/$WORKFLOW_NAME" ]; then
        # Local installation
        echo "  Installing from local files..."
        cp -R "$PROJECT_ROOT/integrations/macos-quick-action/$WORKFLOW_NAME" "$WORKFLOW_DIR/"
        echo -e "${GREEN}✓ Quick Action installed${NC}"
    else
        echo -e "${YELLOW}⚠ Quick Action workflow not found locally${NC}"
        echo "  To install manually, create the workflow following the guide:"
        echo "  $GITHUB_URL/tree/main/integrations/macos-quick-action"
    fi

    echo -e "  Location: ~/Library/Services/${NC}"
    echo -e "  ${YELLOW}Note: You may need to restart Finder${NC}"
    echo
fi

# 3. Install Mac App
if $INSTALL_APP; then
    echo -e "${BOLD}${BLUE}[3/3] Installing Mac App...${NC}"

    APP_DIR="/Applications"
    APP_NAME="Markdown Fixer.app"

    # Check if local app exists
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

    if [ -d "$PROJECT_ROOT/integrations/macos-app/build/$APP_NAME" ]; then
        # Local installation
        echo "  Installing from local files..."
        sudo cp -R "$PROJECT_ROOT/integrations/macos-app/build/$APP_NAME" "$APP_DIR/"
        echo -e "${GREEN}✓ Mac App installed${NC}"
        echo -e "  Location: /Applications/${NC}"
        echo -e "  ${YELLOW}Note: First time, right-click → Open to bypass Gatekeeper${NC}"
    else
        echo -e "${YELLOW}⚠ Mac App not built yet${NC}"
        echo "  To build, run:"
        echo "  cd integrations/macos-app && ./build-py2app.sh"
    fi

    echo
fi

# Summary
echo
echo -e "${BOLD}${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║     Installation Complete! 🎉         ║${NC}"
echo -e "${BOLD}${GREEN}╚════════════════════════════════════════╝${NC}"
echo

echo -e "${BOLD}Usage:${NC}"

if $INSTALL_CLI; then
    echo -e "  ${BOLD}CLI:${NC}"
    echo -e "    markdown-fixer file.md              # Fix a file"
    echo -e "    markdown-fixer file.md -i           # Fix in-place"
    echo -e "    markdown-fixer *.md -i              # Fix multiple files"
    echo -e "    markdown-fixer --help               # Show all options"
    echo
fi

if $INSTALL_QUICK_ACTION; then
    echo -e "  ${BOLD}Quick Action:${NC}"
    echo -e "    1. Right-click any .md file in Finder"
    echo -e "    2. Quick Actions → Fix Markdown"
    echo
fi

if $INSTALL_APP; then
    echo -e "  ${BOLD}Mac App:${NC}"
    echo -e "    Drag .md files onto the Markdown Fixer app"
    echo
fi

echo -e "${BOLD}JetBrains IDE Integration:${NC}"
echo -e "  Setup guide: $GITHUB_URL/tree/main/integrations/jetbrains"
echo

echo -e "${BOLD}Documentation:${NC}"
echo -e "  $GITHUB_URL/blob/main/README.md"
echo

echo -e "${BOLD}Support:${NC}"
echo -e "  Issues: $GITHUB_URL/issues"
echo

# Post-install actions
if $INSTALL_QUICK_ACTION && [ -d "$WORKFLOW_DIR/$WORKFLOW_NAME" ]; then
    echo -e "${YELLOW}Restarting Finder to activate Quick Action...${NC}"
    killall Finder 2>/dev/null || true
    echo -e "${GREEN}✓ Finder restarted${NC}"
    echo
fi

echo "Thank you for using Markdown Fixer!"
