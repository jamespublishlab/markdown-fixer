# Markdown Fixer MCP Server for Claude Desktop

Integrate markdown-fixer directly into Claude Desktop via the Model Context Protocol (MCP).

---

## 🚀 New to This? Start Here!

**Non-technical user?** We have a simple, step-by-step guide just for you:

👉 **[Simple Setup Guide for Non-Technical Users](../../CLAUDE_DESKTOP_SIMPLE_SETUP.md)** 👈

No command line knowledge needed! Just copy, paste, and click.

**Technical user?** Continue reading below for advanced options.

---

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open standard that allows AI assistants like Claude to connect with external tools and data sources. This MCP server exposes markdown-fixer's capabilities directly to Claude Desktop.

## Features

Once installed, Claude Desktop can:

- **Automatically fix markdown** you generate in conversations
- **Fix markdown in artifacts** with a simple request
- **Preview changes** before applying them
- **Fix files** on your local system
- **Detect formatting issues** and suggest fixes

## Installation

### Quick Install (Recommended)

```bash
cd integrations/mcp-server
chmod +x install.sh
./install.sh
```

The installer will:

1. Check if Python and markdown-fixer are installed
2. Install markdown-fixer if needed
3. Configure Claude Desktop automatically
4. Provide next steps

### Manual Installation

#### 1. Install markdown-fixer

```bash
# Install from PyPI (recommended)
pip3 install markdown-fixer

# Or from project root
pip3 install -e .

# Or with pipx
pipx install markdown-fixer
```

#### 2. Configure Claude Desktop

**macOS:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:**
Edit `~/.config/Claude/claude_desktop_config.json`

**Windows:**
Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

**Method 1: pipx (Recommended)**

This is the cleanest approach - pipx creates an isolated environment:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "/Users/YOUR_USERNAME/.local/pipx/venvs/markdown-fixer/bin/python3",
      "args": [
        "-m",
        "markdown_fixer.mcp_server"
      ]
    }
  }
}
```

**Note:** Replace `YOUR_USERNAME` with your actual username. On Windows, the path is `%USERPROFILE%\.local\pipx\venvs\markdown-fixer\Scripts\python.exe`

**Why this is best:**

- Isolated environment (no conflicts with system Python)
- Works globally (not tied to project directory)
- Survives project deletion
- Clean uninstall with `pipx uninstall markdown-fixer`

**Method 2: System Python (Alternative)**

Only if you've installed to system Python (not recommended):

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": [
        "-m",
        "markdown_fixer.mcp_server"
      ]
    }
  }
}
```

**Note:** This only works if markdown-fixer is in your system Python packages

**Method 3: Development Mode (Source Path)**

Only use this if you're actively developing the MCP server code:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": [
        "/absolute/path/to/markdown-fixer/integrations/mcp-server/server.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/markdown-fixer/src"
      }
    }
  }
}
```

**When to use this:**

- You're modifying the MCP server code
- You want to test changes before installing

**Important:** Replace `/absolute/path/to/markdown-fixer` with the actual path.

#### 3. Restart Claude Desktop

Close and reopen Claude Desktop for changes to take effect.

## Usage

### Basic Usage

Once installed, simply ask Claude to fix markdown:

```
User: Can you fix this markdown for me?

**Purpose:** Fix markdown
**Status:** Active
- List item
More text

Too many blank lines
```

Claude will use the `fix_markdown` tool to clean it up automatically!

### Available Tools

The MCP server provides three tools:

#### 1. `fix_markdown` ⭐ Primary Tool
Fixes markdown content directly. **Use this for uploaded files, pasted content, or generated markdown.**

**When to use:**

- Uploaded files (Claude will read them first, then pass content to this tool)
- Content you paste in the conversation
- Markdown Claude generates

**Example:**
```
"Fix this markdown content: [paste your markdown]"
```

#### 2. `fix_markdown_file` 📁 Local Files Only
Fixes markdown files on your local filesystem. **Only works with files in your user directories like ~/Desktop, ~/Documents, ~/Downloads.**

**When to use:**

- Files already on your computer's filesystem
- **NOT for files uploaded to Claude Desktop** (use `fix_markdown` instead)

**Example:**
```
"Fix the markdown file at ~/Documents/README.md"
```

#### 3. `preview_markdown_fixes` 👁️ Preview Changes
Shows what changes would be made without applying them.

**When to use:**

- You want to see changes before applying them
- Reviewing what markdown-fixer would fix

**Example:**
```
"Preview what fixes you'd make to this markdown: [paste content]"
```

### Real-World Examples

#### Fix Uploaded Files (Most Common)

```
User: [Uploads README.md] Can you fix the markdown formatting in this file?

Claude: [uses fix_markdown tool with the file's content]
I've fixed the formatting issues in your README.md:
- Added blank lines around 3 lists
- Converted 4 consecutive field metadata lines to bullets
- Collapsed excessive newlines

[Shows fixed content]
```

#### Fix Generated Content

```
User: Write a README for a Python project

Claude: [generates README with formatting issues]

User: Can you fix the markdown formatting?

Claude: [uses fix_markdown tool automatically]
Here's the fixed version with proper spacing around lists...
```

#### Fix Local System Files

```
User: Fix the markdown file at ~/Documents/notes.md

Claude: [uses fix_markdown_file tool]
I've fixed the formatting in ~/Documents/notes.md. The changes include:
- Added blank lines around 2 lists
- Collapsed excessive newlines
```

#### Preview Before Fixing

```
User: Show me what fixes you'd make to this markdown without changing it

Claude: [uses preview_markdown_fixes tool]
Here's what I would fix:
- Add blank lines around 2 lists (lines 5 and 12)
- Convert 3 consecutive field metadata lines to bullets
- Collapse 4 blank lines to 2
...
```

## What It Fixes

The MCP server uses markdown-fixer's core functionality:

1. **Blank Lines Around Lists** - Adds proper spacing
2. **Field Metadata to Bullets** - Converts `**Key:** value` patterns (2+ consecutive)
3. **Newline Normalization** - Collapses 3+ blank lines to 2
4. **Code Block Preservation** - Never modifies code blocks

## Troubleshooting

### Server Not Appearing

**Check configuration:**
```bash
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cat ~/.config/Claude/claude_desktop_config.json
```

**Verify paths:**

- Ensure paths in config are absolute, not relative
- Check that `server.py` exists at the specified path
- Verify `PYTHONPATH` points to the `src` directory

### Tools Not Working

**Test server directly:**
```bash
# Using module (recommended)
python3 -m markdown_fixer.mcp_server
# Type: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
# Press Enter
# Should see a JSON response

# Or using server.py path
python3 integrations/mcp-server/server.py
```

**Check logs:**

- Open Claude Desktop Developer Tools (if available)
- Look for MCP connection errors
- Check stderr output

### Import Errors

**Ensure markdown-fixer is installed:**
```bash
python3 -c "import markdown_fixer; print(markdown_fixer.__version__)"
```

**If not found:**
```bash
pip install -e /path/to/markdown-fixer
```

### Permission Issues

**Make server executable:**
```bash
chmod +x integrations/mcp-server/server.py
```

### Zod Validation Errors

If you see errors like `ZodError: Invalid input` or `Expected string, received null`:

**Cause:** The MCP server is returning responses that don't match Claude Desktop's expected schema.

**Solution:**

1. Make sure you're using the latest version of the MCP server
2. Restart Claude Desktop completely:
   ```bash
   killall Claude
   # Then reopen Claude Desktop
   ```
3. Check that your server.py is up to date (should handle null IDs gracefully)

**Test the server:**
```bash
npx @modelcontextprotocol/inspector /absolute/path/to/server.py
```

This opens a web interface where you can see all requests/responses and verify the server is working correctly.

## Advanced Configuration

### Custom Python Environment

If using a virtual environment:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/absolute/path/to/server.py"
      ]
    }
  }
}
```

### Multiple Servers

You can run multiple MCP servers:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": ["/path/to/markdown-fixer/integrations/mcp-server/server.py"]
    },
    "other-server": {
      "command": "node",
      "args": ["/path/to/other/server.js"]
    }
  }
}
```

### Environment Variables

Add custom environment variables:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/src",
        "LOG_LEVEL": "DEBUG",
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

## Development

### Testing the Server

```bash
# Run server in stdio mode (module approach)
python3 -m markdown_fixer.mcp_server

# Or using server.py path
python3 integrations/mcp-server/server.py

# Send test request
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 -m markdown_fixer.mcp_server
```

### Debugging

Enable debug logging by editing `server.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    # ...
)
```

### Extending the Server

Add new tools by:

1. Add tool definition in `_handle_tools_list()`
2. Implement handler method
3. Add case in `_handle_tool_call()`

Example:

```python
def _handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
    tools = [
        # ... existing tools ...
        {
            "name": "my_new_tool",
            "description": "Does something cool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                },
                "required": ["param"]
            }
        }
    ]
    # ...
```

## Uninstallation

### Remove from Claude Desktop

Edit your config file and remove the `markdown-fixer` entry:

```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
nano ~/.config/Claude/claude_desktop_config.json
```

### Uninstall markdown-fixer

```bash
pip uninstall markdown-fixer
```

## Architecture

```
Claude Desktop
      ↓
   MCP Protocol (stdio)
      ↓
server.py (MCP Server)
      ↓
markdown_fixer.core.MarkdownFixer
      ↓
Fixed Markdown
```

The server:

- Runs as a subprocess of Claude Desktop
- Communicates via JSON-RPC over stdio
- Calls markdown-fixer's core logic
- Returns results to Claude

## Security Considerations

- **File Access**: The server can read/write files Claude requests
- **System Commands**: No shell commands are executed
- **Data Privacy**: All processing happens locally
- **Sandboxing**: Runs in Python's standard sandbox

## Performance

- **Startup**: < 1 second
- **Processing**: Instant for typical markdown files
- **Memory**: ~10-20 MB
- **No Network**: All processing is local

## Compatibility

- **Claude Desktop**: 1.0.0+
- **Python**: 3.8+
- **OS**: macOS, Linux (Windows support planned)
- **MCP Protocol**: 2024-11-05

## FAQ

**Q: Do I need to restart Claude Desktop after installation?**
A: Yes, Claude Desktop reads the config on startup.

**Q: Can I use this with other AI assistants?**
A: The MCP protocol is standard - any MCP-compatible client should work.

**Q: Does this work offline?**
A: Yes! All processing is local. No internet required.

**Q: Will this slow down Claude?**
A: No, the server is lightweight and only runs when Claude uses the tools.

**Q: Can Claude fix markdown automatically?**
A: Claude decides when to use tools. You can ask it to fix markdown and it will use the appropriate tool.

**Q: Is my data sent anywhere?**
A: No. Everything runs locally on your machine.

## Support

- **Issues**: [GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)
- **MCP Docs**: [Model Context Protocol](https://modelcontextprotocol.io)
- **Main Project**: [markdown-fixer README](../../README.md)

## See Also

- [Main Project Documentation](../../README.md)
- [Claude Code Integration](../../.claude/README.md)
- [Other Integrations](../README.md)

## License

MIT - Same as the parent markdown-fixer project
