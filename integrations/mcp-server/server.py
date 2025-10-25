#!/usr/bin/env python3
"""
MCP Server for markdown-fixer.

This server exposes markdown-fixer functionality to Claude Desktop
via the Model Context Protocol (MCP).
"""

import sys
import json
import logging
from typing import Any, Dict, List
from pathlib import Path

# Try to import markdown_fixer
try:
    from markdown_fixer import MarkdownFixer, __version__
except ImportError:
    # Fallback if not installed - use relative import or embedded version
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))
    from markdown_fixer import MarkdownFixer, __version__

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Log to stderr, MCP uses stdout for protocol
)
logger = logging.getLogger('markdown-fixer-mcp')


class MarkdownFixerMCPServer:
    """MCP Server for markdown-fixer."""

    def __init__(self):
        self.fixer = MarkdownFixer()
        self.server_info = {
            "name": "markdown-fixer",
            "version": __version__
        }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        # If no id, this might be a notification - don't respond
        if request_id is None and method:
            logger.warning(f"Received notification (no id): {method}")
            return None

        logger.info(f"Received request: {method}")

        try:
            if method == "initialize":
                return self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            elif method == "tools/call":
                return self._handle_tool_call(request_id, params)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")
        except Exception as e:
            logger.error(f"Error handling request: {e}", exc_info=True)
            return self._error_response(request_id, -32603, str(e))

    def _handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        logger.info("Initializing server")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": self.server_info
            }
        }

    def _handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Return list of available tools."""
        tools = [
            {
                "name": "fix_markdown",
                "description": "Fix markdown formatting issues in content. USE THIS for uploaded files, content from conversations, or any markdown content you have as a string. This is the PRIMARY tool for most interactions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The markdown content to fix. Can be from uploaded files (read them first), pasted content, or generated text."
                        }
                    },
                    "required": ["content"]
                }
            },
            {
                "name": "fix_markdown_file",
                "description": "Fix markdown formatting in a file on the user's local filesystem. ONLY use for files in user directories like ~/Desktop, ~/Documents, ~/Downloads. Does NOT work with uploaded files in Claude Desktop - use fix_markdown for those instead.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Absolute path to a markdown file on the user's actual filesystem (e.g., /Users/username/Desktop/file.md). NOT for uploaded files."
                        },
                        "in_place": {
                            "type": "boolean",
                            "description": "Whether to modify the file in-place (default: true)",
                            "default": True
                        }
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "preview_markdown_fixes",
                "description": "Preview what formatting changes would be made to markdown content without applying them. Useful for showing users what will change before fixing.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The markdown content to preview fixes for"
                        }
                    },
                    "required": ["content"]
                }
            }
        ]

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }

    def _handle_tool_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        logger.info(f"Calling tool: {tool_name}")

        if tool_name == "fix_markdown":
            return self._fix_markdown(request_id, arguments)
        elif tool_name == "fix_markdown_file":
            return self._fix_markdown_file(request_id, arguments)
        elif tool_name == "preview_markdown_fixes":
            return self._preview_fixes(request_id, arguments)
        else:
            return self._error_response(request_id, -32602, f"Unknown tool: {tool_name}")

    def _fix_markdown(self, request_id: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Fix markdown content."""
        content = arguments.get("content", "")

        if not content:
            return self._error_response(request_id, -32602, "Content is required")

        try:
            fixed_content = self.fixer.fix_string(content)

            # Calculate statistics
            original_lines = len(content.split('\n'))
            fixed_lines = len(fixed_content.split('\n'))

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": fixed_content
                        }
                    ],
                    "isError": False
                }
            }
        except Exception as e:
            logger.error(f"Error fixing markdown: {e}", exc_info=True)
            return self._error_response(request_id, -32603, f"Failed to fix markdown: {str(e)}")

    def _fix_markdown_file(self, request_id: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Fix markdown file."""
        filepath = arguments.get("filepath", "")
        in_place = arguments.get("in_place", True)

        if not filepath:
            return self._error_response(request_id, -32602, "Filepath is required")

        try:
            result_path = self.fixer.fix_file(filepath, in_place=in_place)

            message = f"Fixed markdown file: {result_path}"
            if in_place:
                message = f"Fixed {filepath} in-place"

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        }
                    ],
                    "isError": False
                }
            }
        except FileNotFoundError:
            return self._error_response(request_id, -32602, f"File not found: {filepath}")
        except Exception as e:
            logger.error(f"Error fixing file: {e}", exc_info=True)
            return self._error_response(request_id, -32603, f"Failed to fix file: {str(e)}")

    def _preview_fixes(self, request_id: Any, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Preview markdown fixes without applying them."""
        content = arguments.get("content", "")

        if not content:
            return self._error_response(request_id, -32602, "Content is required")

        try:
            fixed_content = self.fixer.fix_string(content)

            # Check if any changes were made
            if content == fixed_content:
                preview = "No formatting changes needed - markdown is already properly formatted!"
            else:
                # Show basic stats
                original_lines = len(content.split('\n'))
                fixed_lines = len(fixed_content.split('\n'))
                line_diff = fixed_lines - original_lines

                preview = f"Preview of changes:\n\n"
                preview += f"Original: {original_lines} lines\n"
                preview += f"Fixed: {fixed_lines} lines\n"
                preview += f"Difference: {line_diff:+d} lines\n\n"
                preview += "Changes will include:\n"
                preview += "- Blank lines added around lists\n"
                preview += "- Field metadata converted to bullets (if 2+ consecutive)\n"
                preview += "- Excessive newlines collapsed\n\n"
                preview += f"Fixed content:\n\n{fixed_content}"

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": preview
                        }
                    ],
                    "isError": False
                }
            }
        except Exception as e:
            logger.error(f"Error previewing fixes: {e}", exc_info=True)
            return self._error_response(request_id, -32603, f"Failed to preview fixes: {str(e)}")

    def _error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }

    def run(self):
        """Run the MCP server (stdio mode)."""
        logger.info(f"Starting markdown-fixer MCP server v{__version__}")

        try:
            for line in sys.stdin:
                if not line.strip():
                    continue

                try:
                    request = json.loads(line)
                    response = self.handle_request(request)

                    # Write response to stdout (only if there is one)
                    if response is not None:
                        print(json.dumps(response), flush=True)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    # Don't send response for parse errors - client can't match it without an id
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)


def main():
    """Main entry point."""
    server = MarkdownFixerMCPServer()
    server.run()


if __name__ == "__main__":
    main()
