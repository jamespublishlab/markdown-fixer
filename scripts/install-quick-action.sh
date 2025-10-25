#!/bin/bash
# Install macOS Quick Action for Markdown Fixer

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BOLD}Installing Quick Action: Fix Markdown${NC}"
echo

WORKFLOW_DIR="$HOME/Library/Services"
WORKFLOW_NAME="Fix Markdown.workflow"

# Get the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SOURCE_PATH="$PROJECT_ROOT/integrations/macos-quick-action/$WORKFLOW_NAME"

# Check if source exists
if [ ! -d "$SOURCE_PATH" ]; then
    echo -e "${YELLOW}⚠ Workflow not found at $SOURCE_PATH${NC}"
    echo
    echo "The Quick Action workflow needs to be created manually using Automator."
    echo "Please follow the instructions in:"
    echo "  $PROJECT_ROOT/integrations/macos-quick-action/README.md"
    echo
    echo "Or create it now:"
    echo "  1. Open Automator"
    echo "  2. Create new Quick Action"
    echo "  3. Copy the script from quick-action-script.sh"
    echo "  4. Save as 'Fix Markdown'"
    exit 1
fi

# Create Services directory if it doesn't exist
mkdir -p "$WORKFLOW_DIR"

# Remove existing workflow if present
if [ -d "$WORKFLOW_DIR/$WORKFLOW_NAME" ]; then
    echo "Removing existing workflow..."
    rm -rf "$WORKFLOW_DIR/$WORKFLOW_NAME"
fi

# Copy workflow
echo "Copying workflow..."
cp -R "$SOURCE_PATH" "$WORKFLOW_DIR/"

echo -e "${GREEN}✓ Quick Action installed!${NC}"
echo
echo "Usage:"
echo "  1. Right-click any .md file in Finder"
echo "  2. Quick Actions → Fix Markdown"
echo
echo "Note: You may need to restart Finder for changes to take effect:"
echo "  killall Finder"
