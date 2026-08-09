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
        "matcher": "^Write$|^mcp__obsidian-mcp-tools__(create|patch|append).*$",
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

**The matcher lists `Write` only, and that is not an oversight.** The hook
reads the new file content from `tool_input.content`. `Write` carries that key;
`Edit` does not — it sends `old_string`/`new_string` — so the hook exits
immediately on every edit and can never rewrite one. Listing `Edit` in the
matcher advertised a capability the code cannot deliver. **Editing an existing
markdown file is therefore never auto-fixed; only whole-file writes are.**
(`Update` was listed too and is not a tool in Claude Code at all.)

The hook is **opt-in**: this line alone does nothing. Arm it per machine,
either with `~/.config/markdown-fixer/config.json`:

```json
{
  "hook_enabled": true,
  "exclude_patterns": ["(^|/)(Daily|Weekly)/"],
  "strip_horizontal_rules": false
}
```

**Every manipulation has its own key, and defaults differ by surface.** A key's
*presence* makes it global; its *absence* leaves each surface to its own default:

| Fix | hook | cli/mcp |
|:--|:--|:--|
| `blank_lines_around_blocks` | on | on |
| `collapse_blank_runs` | on | on |
| `bullet_field_metadata` | **off** | on |
| `reflow_tables` | **off** | on |
| `strip_horizontal_rules` | **off** | on |

The hook fires automatically on writes Claude makes, so it does whitespace
hygiene only — anything that restructures or deletes visible content is opt-in.
The CLI and the MCP tools are direct requests to reformat, so they run
everything. Setting a key in the config applies it to every surface.

**Setting a key in the config applies it everywhere.** To change the hook
*only*, set `MARKDOWN_FIXER_FIXES` on the hook's own command line — an env var
exists only in that process, so it cannot bleed into your CLI:

```json
"command": "command -v markdown-fixer >/dev/null 2>&1 && MARKDOWN_FIXER_FIXES='{\"reflow_tables\": true}' markdown-fixer hook claude-code || true"
```

Precedence is `surface default < config file (global) < env var (per-process)`.

Run `markdown-fixer doctor` to see how each fix resolves on each surface and
which layer it came from.

or with the environment variable `MARKDOWN_FIXER_HOOK=1`. Setting
`MARKDOWN_FIXER_HOOK=0` forces it off regardless of the config file. Run
`markdown-fixer doctor` to see which route armed it (if any), and which
exclusion patterns it will apply.

Write patterns to match **both** path shapes the matcher's tools can send:
`Write` supplies an absolute path, but the Obsidian MCP tools
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

- A `PreToolUse` hook intercepts `Write` and the Obsidian MCP
  create/patch/append tools before they run
- **Whole-file writes only.** `Edit` sends `old_string`/`new_string` rather
  than `content`, so the hook cannot act on it and exits immediately
- Only processes `.md` files
- Leaves `---` rules alone unless `strip_horizontal_rules` is set true
- Only runs when armed on that machine (opt-in — see [hooks/README.md](hooks/README.md))
- Only active if markdown-fixer is on `PATH`

## Usage Comparison

| Method | Best For | Example |
|--------|----------|---------|
| **Slash commands** | Quick, specific operations | `/fix-markdown README.md` |
| **Skill** | Complex workflows, AI-guided | "Fix all docs but show me changes first" |
| **Auto-fix hook** | Automatic, hands-off | Write a new file → auto-fixed (edits are not) |
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
