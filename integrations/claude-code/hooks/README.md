# Claude Code Hooks

The `PreToolUse` hook that integrates markdown-fixer with Claude Code. It is
built into the `markdown-fixer` binary as the `hook claude-code` subcommand —
there is no longer a standalone script in this directory to install.

## Installation

### 1. Install markdown-fixer

```bash
git clone https://github.com/jamespublishlab/markdown-fixer
cd markdown-fixer
./scripts/install-all.sh --cli     # builds and installs ~/.local/bin/markdown-fixer
```

On Linux, `install-all.sh` is macOS-only — build with `scripts/build-zipapp.sh`
and put the artifact on your `PATH` by hand.

### 2. Configure Claude Code

Add to `~/.claude/settings.json` under `hooks.PreToolUse` — this line is
identical on every machine and contains no paths:

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

### 3. Arm it

The hook is **opt-in**. It does nothing until armed on that machine, either by
`~/.config/markdown-fixer/config.json` (or
`$XDG_CONFIG_HOME/markdown-fixer/config.json`):

```json
{
  "hook_enabled": true,
  "exclude_patterns": ["(^|/)(Daily|Weekly)/"]
}
```

or by setting `MARKDOWN_FIXER_HOOK=1` in the environment that runs Claude
Code. Setting `MARKDOWN_FIXER_HOOK=0` forces it off regardless of the config
file. A malformed config file forces it unarmed as well, even against a
truthy env var — an unreadable config means the exclusion set is unknown, and
running with silently-empty exclusions is the wrong direction to fail in.

**Write which path form your patterns need to match.** `Write` and `Edit`
supply an **absolute** path (e.g.
`/Users/you/Documents/SecondBrain/Daily/x.md`); the Obsidian MCP tools
(`mcp__obsidian-mcp-tools__create_vault_file` and friends) supply a
**vault-relative** path instead (e.g. `Daily/x.md`), because that's the form
the plugin's own API takes. A pattern anchored with `^~/…` or `^/Users/…`
therefore matches the first and **silently never matches the second** — a
config written that way looks correct, `markdown-fixer doctor` reports it as
`ok`, and it still does not protect notes an Obsidian MCP tool writes.
Patterns are matched with `re.search` (unanchored), so an anchor-free form
like `(^|/)(Daily|Weekly)/` matches both path shapes and is the recommended
style for anything the Obsidian MCP tools can also write to.

Run `markdown-fixer doctor` to see which route armed it (if any), what
config file it's reading, and which exclusion patterns are active.

## How It Works

### `hook claude-code` (PreToolUse)

- **Trigger:** Before Claude uses Write, Edit, Update, or the Obsidian MCP
  create/patch/append tools
- **Purpose:** Clean markdown content before it's written to disk

**What it does:**

1. Receives a `PreToolUse` JSON payload on stdin
2. Returns immediately, doing nothing, unless the hook is armed on this
   machine
3. Gates strictly on the file having a `.md` extension — content-based
   sniffing was deliberately rejected because it false-positives on
   `#`-commented code (shell, Python, YAML, Dockerfiles)
4. Skips the file if its path matches one of the configured
   `exclude_patterns` (each pattern is tested with `re.search`, against both
   the literal path and its `~`-collapsed form)
5. Runs markdown-fixer on the content; if the result differs, returns it via
   `updatedInput`
6. Always exits 0 — a hook failure must never block a write, so any error
   along the way is swallowed and the original content passes through
   untouched

### Hook Lifecycle

1. **Claude prepares to write/edit** → Hook intercepts
2. **Hook receives JSON** → Contains `tool_name`, `tool_input` with content
3. **Hook checks arming, extension, and exclusions**
4. **Hook cleans content** → Runs markdown-fixer
5. **Hook returns** → `updatedInput` with cleaned content, only if it changed
6. **Tool executes** → Writes the already-cleaned content

### Input Format

The hook receives JSON via stdin:

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.md",
    "content": "..."
  }
}
```

The Obsidian MCP tools use `filename` instead of `file_path`; the hook checks
both.

### Output Format

If content is modified:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "content": "...cleaned content..."
    }
  }
}
```

If the content is unchanged, the hook prints nothing.

## Supported Tools

The `matcher` regex above intercepts:

- **Write** - Creating new files
- **Edit** - Modifying existing files
- **Update** - Modifying existing files (some clients use this name)
- **mcp__obsidian-mcp-tools__create_vault_file** - Creating Obsidian notes
- **mcp__obsidian-mcp-tools__patch_vault_file** - Modifying Obsidian notes
- **mcp__obsidian-mcp-tools__append_to_vault_file** - Appending to Obsidian notes

## Excluding Files

Exclusions are regex patterns, not a script to edit. Add them to
`exclude_patterns` in the config file, or add more at the environment level
with `MARKDOWN_FIXER_EXCLUDE_PATTERNS` (a JSON array of regex strings — these
add to the config's patterns, they don't replace them):

```bash
export MARKDOWN_FIXER_EXCLUDE_PATTERNS='["(^|/)(Daily|Weekly)/"]'
```

An invalid regex is reported to stderr and skipped; it does not stop the
other patterns from applying. `markdown-fixer doctor` lists every pattern,
its source (config or env), and whether it compiled — including as `ok` for
a pattern that compiles but happens to be anchored to the wrong path shape
for one of the two callers (see [Arm it](#3-arm-it) above); `doctor` checks
that a pattern is valid regex, not that it matches what you intend.

## Troubleshooting

### Hook Not Running

1. Run `markdown-fixer doctor` and check the `hook` line — it reports
   exactly what armed it, or why it did not arm

2. Check `~/.claude/settings.json` has the `PreToolUse` entry configured
   correctly (see [Installation](#installation) above)

3. Check `markdown-fixer` is on `PATH` — the settings.json command resolves
   it with `command -v`, same as your shell would

Note: `doctor` runs in your shell with your `PATH`, but Claude Code's hook
subprocess inherits its parent process's environment instead, which can
differ. `doctor` can't see that environment, only your own shell's.

### Testing Manually

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.md", "content": "# Header\ntext"}}' | markdown-fixer hook claude-code
```

Nothing will print unless the hook is armed (see Step 3 above) and the
content actually changes.

### Enable/Disable

To disable everywhere: remove the `PreToolUse` entry from
`~/.claude/settings.json`.

To disable on just one machine while keeping the settings.json entry
(identical on every machine) intact: set `hook_enabled` to `false` (or
delete it) in that machine's config file, and don't set
`MARKDOWN_FIXER_HOOK=1`. `MARKDOWN_FIXER_HOOK=0` forces it off unconditionally.

## See Also

- [Claude Code Integration](../README.md) - All Claude Code components
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
