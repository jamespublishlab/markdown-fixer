# Integrations

markdown-fixer integrates with multiple platforms and workflows. Choose the integration that fits how you work.

## Quick Comparison

| Integration | Best For | Platform |
|-------------|----------|----------|
| [CLI](#command-line) | Terminal users, scripts, CI/CD | All |
| [macOS Quick Action](#macos-quick-action) | Right-click in Finder | macOS |
| [macOS App](#macos-drag-and-drop-app) | Drag-and-drop files | macOS |
| [JetBrains Plugin](#jetbrains-plugin) | IDE users (PyCharm, IntelliJ, etc.) | All |
| [Claude Code](#claude-code) | AI-assisted development | All |
| [Claude Desktop](#claude-desktop-mcp) | Claude Desktop app users | All |

## Command Line

The CLI is installed automatically with the Python package.

```bash
markdown-fixer file.md --in-place
```

See [Usage Guide](usage.md) for complete CLI documentation.

## macOS Quick Action

Adds "Fix Markdown" to Finder's right-click menu.

**How to use:**

1. Right-click any `.md` file in Finder
2. Quick Actions > Fix Markdown
3. File is fixed in-place

**Setup:** [Quick Action Guide](../integrations/macos-quick-action/README.md)

## macOS Drag-and-Drop App

A standalone app that fixes markdown files when you drag them onto it.

**How to use:**

1. Drag `.md` files onto the app icon
2. Files are fixed in-place
3. Notification confirms completion

**Setup:** [macOS App Guide](../integrations/macos-app/README.md)

## JetBrains Plugin

Native plugin for JetBrains IDEs (PyCharm, IntelliJ IDEA, PhpStorm, WebStorm, etc.).

**How to use:**

1. Right-click any `.md` file
2. Fix Markdown Formatting
3. File is fixed in-place

**Features:**

- Context menu integration
- Multiple file selection support
- Keyboard shortcuts

**Setup:** [JetBrains Plugin Guide](../integrations/jetbrains-plugin/README.md)

## Claude Code

Three integration methods for Claude Code users:

### Slash Commands

```
/fix-markdown README.md
/fix-all-markdown
```

### AI Skill

Ask naturally:

```
"Fix all markdown files but show me the changes first"
"Which markdown files need fixing?"
```

### Auto-Fix Hook

Automatically fixes markdown files after Claude writes or edits them.

**Setup:** [Claude Code Guide](../integrations/claude-code/README.md)

## Claude Desktop (MCP)

Integrate via Model Context Protocol for Claude Desktop.

**How to use:**

Just ask Claude:

```
"Fix this markdown: **Name:** John **Age:** 30"
"Fix the file at ~/Documents/README.md"
"Preview changes to this markdown content"
```

**For non-technical users:** [Simple Setup Guide](claude-desktop-setup.md)

**Full documentation:** [MCP Server Guide](../integrations/mcp-server/README.md)

## Choosing an Integration

### For Individual Files

- **Quick fix:** CLI (`markdown-fixer file.md -i`)
- **Visual workflow:** macOS Quick Action or App
- **In your IDE:** JetBrains Plugin

### For Batch Processing

- **Scripts/CI:** CLI with glob patterns
- **AI-assisted:** Claude Code slash commands

### For AI Workflows

- **Claude Code users:** Slash commands, skill, or auto-fix hook
- **Claude Desktop users:** MCP Server integration

## See Also

- [Installation](installation.md) - Install the core tool
- [Usage Guide](usage.md) - CLI and library reference
- [Troubleshooting](troubleshooting.md) - Common issues
