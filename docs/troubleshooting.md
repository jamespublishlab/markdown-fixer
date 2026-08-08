# Troubleshooting

Solutions to common issues with markdown-fixer.

## Installation Issues

### "command not found"

The `markdown-fixer` command isn't in your PATH.

**Solution 1:** Reinstall the zipapp (macOS) and check the installer's PATH warning

```bash
./scripts/install-all.sh --cli
```

If `~/.local/bin` isn't on your PATH, the installer prints a warning — the
Claude Code hook resolves `markdown-fixer` via PATH too, so it will silently
do nothing until this is fixed.

**Solution 2:** Add to PATH

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc  # or source ~/.zshrc
```

**Solution 3:** Run as Python module (requires `pip install`, see below)

```bash
python -m markdown_fixer.cli file.md -i
```

### "No module named 'markdown_fixer'"

This only applies if you installed with `pip` (the zipapp is self-contained
and doesn't need the package importable). The package isn't installed in
your Python environment:

```bash
pip install git+https://github.com/jamespublishlab/markdown-fixer.git
# or if installing from source:
pip install -e .
```

### "Permission denied" on scripts

```bash
chmod +x scripts/install-all.sh
chmod +x scripts/build-zipapp.sh
```

## Usage Issues

### Changes don't look right

**Check the file extension:** Only `.md` files are processed

**Try dry-run first:**

```bash
markdown-fixer file.md --dry-run
```

**Check for code blocks:** Content inside ` ```...``` ` is never modified

### File not being modified

**Check write permissions:**

```bash
ls -la file.md
```

**Try explicit in-place flag:**

```bash
markdown-fixer file.md --in-place
```

### Want to undo changes

**If using git:**

```bash
git checkout file.md
```

**From backup:**

```bash
cp file.md.backup file.md
```

**Tip:** Use the default behavior (creates `.formatted.md`) to preview:

```bash
markdown-fixer file.md  # Creates file.formatted.md
# Review, then:
mv file.formatted.md file.md
```

## Platform-Specific Issues

### macOS Quick Action

**Not appearing in menu:**

1. Open System Settings > Privacy & Security > Extensions
2. Enable "Quick Actions" for Automator
3. Restart Finder: `killall Finder`

**See:** [Quick Action Guide](../integrations/macos-quick-action/README.md)

### macOS App

**"App is damaged" warning:**

```bash
xattr -cr /Applications/Markdown\ Fixer.app
```

**See:** [macOS App Guide](../integrations/macos-app/README.md)

### JetBrains Plugin

**Not appearing in context menu:**

1. Check plugin is installed: Settings > Plugins
2. Restart IDE
3. Try right-clicking on a `.md` file specifically

**See:** [JetBrains Guide](../integrations/jetbrains-plugin/README.md)

### Claude Code

**Slash commands not working:**

```bash
# Verify installation
which markdown-fixer
```

**Auto-fix hook not running:**

The hook is opt-in and armed per machine — see whether it's armed, and by
what:

```bash
markdown-fixer doctor
```

Also check `~/.claude/settings.json` has the `PreToolUse` hook entry.

**See:** [Claude Code Hooks Guide](../integrations/claude-code/hooks/README.md)

### Claude Desktop (MCP)

**Server not connecting:**

1. Restart Claude Desktop completely
2. Check configuration in `~/Library/Application Support/Claude/claude_desktop_config.json`
3. Check server logs

**See:** [MCP Server Guide](../integrations/mcp-server/README.md)

## Getting Help

### Check existing issues

[GitHub Issues](https://github.com/jamespublishlab/markdown-fixer/issues)

### Open a new issue

Include:

1. Your OS and Python version: `python --version`
2. markdown-fixer version: `markdown-fixer --version`
3. Example input markdown
4. Expected vs actual output
5. Full error message (if any)

### Debugging

Run with verbose output:

```bash
markdown-fixer file.md -i -v
```

Check Python version:

```bash
python --version
which python
```

Check installation location:

```bash
pip show markdown-fixer
```

## See Also

- [Installation](installation.md) - Installation methods
- [Usage Guide](usage.md) - CLI and library reference
- [Integrations](integrations.md) - Platform-specific guides
