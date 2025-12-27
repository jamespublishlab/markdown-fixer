#!/usr/bin/env python3
"""
MCP Server for markdown-fixer.

This module provides backward compatibility by delegating to the canonical
implementation at integrations/mcp-server/server.py.

This allows:
- `python -m markdown_fixer.mcp_server` to continue working
- Existing config files referencing `markdown_fixer.mcp_server` to work
- Tests importing from `markdown_fixer.mcp_server` to work
"""

import sys
from pathlib import Path

# Add integrations/mcp-server to path so we can import from there
_integrations_path = Path(__file__).parent.parent.parent / "integrations" / "mcp-server"
if _integrations_path.exists():
    sys.path.insert(0, str(_integrations_path))

# Import and re-export from canonical location
from server import MarkdownFixerMCPServer, main

__all__ = ["MarkdownFixerMCPServer", "main"]

if __name__ == "__main__":
    main()
