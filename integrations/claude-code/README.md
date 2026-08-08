# Claude Code Integration

Claude Code integrations for markdown-fixer: slash commands, skill, and auto-fix hook.

## Installation

### 1. Install markdown-fixer

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --cli     # builds and installs ~/.local/bin/markdown-fixer
```

`pip install .` still works and is required only if you want to invoke
`python -m markdown_fixer.mcp_server` directly; the zipapp's supported entry
for that is `markdown-fixer mcp-server`. On Linux, `install-all.sh` is
macOS-only — build with `scripts/build-zipapp.sh` and copy the artifact onto
your `PATH` by hand instead.

### 2. Install Claude Code Components

Copy the components you want to your Claude Code configuration:

**Slash Commands:**
```bash
# Copy to your global Claude Code commands
cp -r commands/ ~/.claude/commands/
```

**Skill:**
```bash
# Copy to your global Claude Code skills
mkdir -p ~/.claude/skills/
cp skill/markdown-fixer ~/.claude/skills/
```

**Auto-Fix Hook:**

The hook is built into the `markdown-fixer` binary — there is no separate
script to copy. Add this line to your `~/.claude/settings.json` under
`hooks.PreToolUse`. It is identical on every machine and contains no paths:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Update|mcp__obsidian-mcp-tools__(create|patch|append).*",
        "hooks": [
          {
            "type": "command",
            "command": "command -v markdown-fixer >/dev/null 2>&1 && markdown-fixer hook claude-code || true"
          }
        ]
      }
    ]
  }
}
```

The hook is **opt-in**: this line alone does nothing. Arm it per machine,
either with `~/.config/markdown-fixer/config.json`:

```json
{
  "hook_enabled": true,
  "exclude_patterns": ["(^|/)(Daily|Weekly)/"]
}
```

or with the environment variable `MARKDOWN_FIXER_HOOK=1`. Setting
`MARKDOWN_FIXER_HOOK=0` forces it off regardless of the config file. Run
`markdown-fixer doctor` to see which route armed it (if any), and which
exclusion patterns it will apply.

Write patterns to match **both** path shapes the matcher's tools can send:
`Write`/`Edit` supply an absolute path, but the Obsidian MCP tools
(`mcp__obsidian-mcp-tools__…`) supply a path relative to the vault root
instead (e.g. `Daily/x.md`, not `/Users/you/…/Daily/x.md`). A pattern
anchored with `^~/…` matches only the first. Since patterns are matched
unanchored (`re.search`), the anchor-free form above — `(^|/)(Daily|Weekly)/`
— matches both. See
[hooks/README.md](hooks/README.md#3-arm-it) for the full explanation.

## Components

### Slash Commands (`commands/`)

Quick commands for common operations.

| Command | Description |
|---------|-------------|
| `/fix-markdown [file]` | Fix specific file(s) |
| `/fix-all-markdown` | Fix all markdown files in project |

**Usage:**
```
/fix-markdown README.md
/fix-markdown docs/*.md
/fix-all-markdown
```

### Skill (`skill/`)

AI-guided markdown fixing workflows. The skill enables Claude Code to:

- Automatically detect formatting issues
- Preview changes before applying
- Work with multiple files intelligently

**Usage:**
```
"Fix all markdown files but show me what changes first"
"Which markdown files need fixing?"
```

### Auto-Fix Hook (`hooks/`)

Cleans markdown content before Claude writes it to disk. See
[hooks/README.md](hooks/README.md) for the full arming and configuration
details.

**How it works:**

- A `PreToolUse` hook intercepts Write, Edit, Update, and the Obsidian MCP
  create/patch/append tools before they run
- Only processes `.md` files
- Only runs when armed on that machine (opt-in — see [hooks/README.md](hooks/README.md))
- Only active if markdown-fixer is on `PATH`

## Usage Comparison

| Method | Best For | Example |
|--------|----------|---------|
| **Slash commands** | Quick, specific operations | `/fix-markdown README.md` |
| **Skill** | Complex workflows, AI-guided | "Fix all docs but show me changes first" |
| **Auto-fix hook** | Automatic, hands-off | Edit file → auto-fixed |
| **Manual CLI** | One-off, custom commands | `markdown-fixer *.md -i` |

## Troubleshooting

### Commands not working?

Check markdown-fixer installation:
```bash
which markdown-fixer
markdown-fixer --version
```

### Hook not running?

1. Confirm it's armed and see what it will skip:
   ```bash
   markdown-fixer doctor
   ```

2. Check `~/.claude/settings.json` has the `PreToolUse` entry configured (see
   [Installation](#installation) above)

3. Ensure `markdown-fixer` is on your `PATH` — the hook command resolves it
   with `command -v`, same as your shell

## See Also

- [Main Documentation](../../README.md)
- [Installation Guide](../../docs/installation.md)
- [Usage Guide](../../docs/usage.md)
