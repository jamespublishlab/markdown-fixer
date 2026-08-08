# Markdown Fixer MCP Server for Claude Desktop

Integrate markdown-fixer directly into Claude Desktop via the Model Context Protocol (MCP).

---

## 🚀 New to This? Start Here!

**Non-technical user?** We have a simple, step-by-step guide just for you:

👉 **[Claude Desktop Setup Guide](../../docs/claude-desktop-setup.md)** 👈

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

### 1. Install markdown-fixer

**macOS (recommended):** build and install the zipapp CLI first — the MCP
server ships inside it as the `mcp-server` subcommand:

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --cli     # builds and installs ~/.local/bin/markdown-fixer
```

**Linux:** `install-all.sh` is macOS-only. Build the artifact with
`scripts/build-zipapp.sh` and copy `dist/markdown-fixer` onto your `PATH` by
hand — it carries a `/usr/bin/env python3` shebang and needs no venv.

**Windows, or if you'd rather use `pip`:**

```bash
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
```

This also works on macOS/Linux and is required if you want to invoke the
server as `python -m markdown_fixer.mcp_server` instead of through the
zipapp's `mcp-server` subcommand.

### 2. Configure Claude Desktop

**macOS:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:**
Edit `~/.config/Claude/claude_desktop_config.json`

**Windows:**
Edit `%APPDATA%\Claude\claude_desktop_config.json`

**If you installed the zipapp (macOS/Linux), add this:**

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "/Users/YOUR_USERNAME/.local/bin/markdown-fixer",
      "args": ["mcp-server"]
    }
  }
}
```

Replace `YOUR_USERNAME` with your actual username. **The path must be
absolute** — Claude Desktop is a GUI app that inherits launchd's environment,
not your shell's. Its actual `PATH` is `/usr/bin:/bin:/usr/sbin:/sbin`, which
contains neither `~/.local/bin` nor Homebrew, so a bare `"command":
"markdown-fixer"` will not resolve. A future edit that "simplifies" this back
to a bare command will silently break the integration.

**If you installed with `pip` (Windows, or by choice on macOS/Linux):**

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "python3",
      "args": ["-m", "markdown_fixer.mcp_server"]
    }
  }
}
```

On Windows, use `"command": "python"` instead — see
[config-templates/windows-config.json](config-templates/windows-config.json).

### 3. Restart Claude Desktop

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

- Ensure the `command` path in your config is absolute, not relative or bare
- If you're using the zipapp form, confirm the path exists: `ls -la ~/.local/bin/markdown-fixer`
- If you're using the `pip`/module form, confirm the module resolves with the same Python `command` names (see below)

### Tools Not Working

**Test the server directly:**
```bash
# Zipapp form
~/.local/bin/markdown-fixer mcp-server
# Type: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
# Press Enter
# Should see a JSON response

# pip-installed / module form
python3 -m markdown_fixer.mcp_server
```

**Check logs:**

- Open Claude Desktop Developer Tools (if available)
- Look for MCP connection errors
- Check stderr output

### Import Errors (pip / module form only)

**Ensure markdown-fixer is installed:**
```bash
python3 -c "import markdown_fixer; print(markdown_fixer.__version__)"
```

**If not found:**
```bash
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
```

### Zod Validation Errors

If you see errors like `ZodError: Invalid input` or `Expected string, received null`:

**Cause:** The MCP server is returning responses that don't match Claude Desktop's expected schema.

**Solution:**

1. Make sure you're using the latest version (rebuild the zipapp, or `git pull` and reinstall)
2. Restart Claude Desktop completely:
   ```bash
   killall Claude
   # Then reopen Claude Desktop
   ```

## Advanced Configuration

### Environment Variables

Claude Desktop launches the server as its own subprocess, so it does not
inherit your shell's environment. Pass anything the server needs explicitly:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "/Users/YOUR_USERNAME/.local/bin/markdown-fixer",
      "args": ["mcp-server"],
      "env": {
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

### Multiple Servers

You can run multiple MCP servers side by side:

```json
{
  "mcpServers": {
    "markdown-fixer": {
      "command": "/Users/YOUR_USERNAME/.local/bin/markdown-fixer",
      "args": ["mcp-server"]
    },
    "other-server": {
      "command": "node",
      "args": ["/path/to/other/server.js"]
    }
  }
}
```

## Development

### Testing the Server

```bash
# Run the server in stdio mode
python3 -m markdown_fixer.mcp_server
# or, against a built zipapp:
dist/markdown-fixer mcp-server

# Send a test request
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 -m markdown_fixer.mcp_server
```

The implementation lives in `src/markdown_fixer/mcp_server.py`.

### Extending the Server

Add new tools by:

1. Add a tool definition in `_handle_tools_list()`
2. Implement a handler method
3. Add a case in `_handle_tool_call()`

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

If you installed the zipapp:

```bash
rm -f ~/.local/bin/markdown-fixer ~/.local/bin/mdfixer
```

If you installed with pip:

```bash
pip uninstall markdown-fixer
```

## Architecture

```
Claude Desktop
      ↓
   MCP Protocol (stdio)
      ↓
markdown_fixer.mcp_server (MCP Server)
      ↓
markdown_fixer.core.MarkdownFixer
      ↓
Fixed Markdown
```

The server:

- Runs as a subprocess of Claude Desktop, invoked either via the zipapp's
  `mcp-server` subcommand or as `python -m markdown_fixer.mcp_server`
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
- **OS**: macOS and Linux (zipapp or `pip install`); Windows (`pip install`)
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
- [Claude Code Integration](../claude-code/README.md)
- [Other Integrations](../README.md)

## License

MIT - Same as the parent markdown-fixer project
