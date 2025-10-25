#!/bin/bash
# Install markdown-fixer MCP server for Claude Desktop

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BOLD}${BLUE}Installing markdown-fixer MCP Server for Claude Desktop${NC}"
echo

# Get absolute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SERVER_PATH="$SCRIPT_DIR/server.py"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Claude"
else
    echo -e "${RED}Unsupported OS: $OSTYPE${NC}"
    echo "This installer supports macOS and Linux only."
    exit 1
fi

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3.8 or later"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if markdown-fixer is installed
echo
echo -e "${BLUE}Checking markdown-fixer installation...${NC}"
if python3 -c "import markdown_fixer" 2>/dev/null; then
    echo -e "${GREEN}✓ markdown-fixer is already installed${NC}"
else
    echo -e "${YELLOW}⚠ markdown-fixer not found, installing...${NC}"
    cd "$PROJECT_ROOT"
    pip3 install -e . || {
        echo -e "${RED}✗ Failed to install markdown-fixer${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ markdown-fixer installed${NC}"
fi

# Make server executable
chmod +x "$SERVER_PATH"

# Create config directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Generate config
echo
echo -e "${BLUE}Configuring Claude Desktop...${NC}"

# Create or update config file
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}⚠ Config file already exists: $CONFIG_FILE${NC}"
    echo "Backing up to ${CONFIG_FILE}.backup"
    cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"

    # Check if markdown-fixer is already configured
    if grep -q '"markdown-fixer"' "$CONFIG_FILE"; then
        echo -e "${YELLOW}⚠ markdown-fixer already configured${NC}"
        echo "To reconfigure, edit: $CONFIG_FILE"
    else
        echo -e "${BLUE}Adding markdown-fixer to existing config...${NC}"
        # This is tricky - we need to merge JSON
        # For now, just show instructions
        echo -e "${YELLOW}Please manually add this to your config:${NC}"
        echo
        cat << EOF
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": [
        "$SERVER_PATH"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_ROOT/src"
      }
    }
  }
}
EOF
    fi
else
    # Create new config
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": [
        "$SERVER_PATH"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_ROOT/src"
      }
    }
  }
}
EOF
    echo -e "${GREEN}✓ Created config file: $CONFIG_FILE${NC}"
fi

echo
echo -e "${BOLD}${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║     Installation Complete! 🎉         ║${NC}"
echo -e "${BOLD}${GREEN}╚════════════════════════════════════════╝${NC}"
echo

echo -e "${BOLD}Next Steps:${NC}"
echo
echo "1. ${BOLD}Restart Claude Desktop${NC}"
echo "   Close and reopen the Claude Desktop app"
echo
echo "2. ${BOLD}Test the integration${NC}"
echo "   Ask Claude: 'Can you fix this markdown for me?'"
echo "   Then provide some poorly formatted markdown"
echo
echo "3. ${BOLD}Available Tools:${NC}"
echo "   - fix_markdown - Fix markdown content"
echo "   - fix_markdown_file - Fix a markdown file"
echo "   - preview_markdown_fixes - Preview changes"
echo

echo -e "${BOLD}Configuration:${NC}"
echo "Config file: $CONFIG_FILE"
echo "Server path: $SERVER_PATH"
echo

echo -e "${BOLD}Troubleshooting:${NC}"
echo "View logs: Check Claude Desktop developer console"
echo "Test server: python3 $SERVER_PATH"
echo "Uninstall: Remove 'markdown-fixer' entry from $CONFIG_FILE"
echo

echo "Documentation: $SCRIPT_DIR/README.md"
