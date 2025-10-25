# Claude Code Hooks

This directory contains hooks that integrate markdown-fixer with Claude Code's workflow.

## Available Hooks

### `user-prompt-submit.sh`

- **Trigger:** After each user prompt submission
- **Purpose:** Automatically fix markdown formatting after edits

**What it does:**

1. Detects if markdown-fixer is installed (silently skips if not)
2. Finds markdown files that were recently modified
3. Runs markdown-fixer on them automatically
4. Operates silently (no output unless errors)

**When it runs:**

- After you edit a markdown file and submit a prompt
- Only on .md files that have been modified
- Only if markdown-fixer is installed

## Configuration

### Enable/Disable Auto-Fix

**To enable (default):**
```bash
# The hook is already enabled by being in this directory
# Just ensure markdown-fixer is installed:
pip install -e .
```

**To disable temporarily:**
```bash
# Rename the hook to disable it
mv .claude/hooks/user-prompt-submit.sh .claude/hooks/user-prompt-submit.sh.disabled
```

**To re-enable:**
```bash
# Rename it back
mv .claude/hooks/user-prompt-submit.sh.disabled .claude/hooks/user-prompt-submit.sh
```

**To disable permanently:**
```bash
# Delete the hook
rm .claude/hooks/user-prompt-submit.sh
```

### Customize Behavior

Edit `user-prompt-submit.sh` to customize:

**Change verbosity:**
```bash
# Current (silent):
markdown-fixer "$file" --in-place --quiet 2>/dev/null

# Show output:
markdown-fixer "$file" --in-place --verbose
```

**Change file detection:**
```bash
# Current: Files modified in last 2 minutes
find . -maxdepth 2 -name "*.md" -mmin -2 -type f

# All markdown files:
find . -name "*.md" -type f

# Specific directories only:
find ./docs -name "*.md" -type f
```

**Add exclusions:**
```bash
# Skip certain files or directories
modified_files=$(git diff --name-only --diff-filter=M | grep '\.md$' | grep -v 'CHANGELOG.md')
```

## How It Works

### Hook Lifecycle

1. **User submits prompt** → Claude Code responds
2. **Hook triggers** → After prompt processing
3. **Hook checks** → Are there modified markdown files?
4. **Hook acts** → Runs markdown-fixer if needed
5. **Hook exits** → Silently (no interruption)

### Git Integration

If you're in a git repository:

- Only fixes files tracked by git
- Only fixes files with uncommitted changes
- Uses `git diff` to detect modifications

If not in a git repo:

- Fixes any .md files modified in the last 2 minutes
- Limited to current and one level of subdirectories

### Safety Features

- **Graceful degradation**: Skips if markdown-fixer not installed
- **Error suppression**: Doesn't fail if files are missing
- **Silent operation**: No spam in the output
- **Non-blocking**: Doesn't interfere with Claude Code

## Troubleshooting

### Hook Not Running

**Check if hooks are enabled:**
```bash
# Verify the hook file exists and is executable
ls -la .claude/hooks/user-prompt-submit.sh
```

**Ensure it's executable:**
```bash
chmod +x .claude/hooks/user-prompt-submit.sh
```

**Check if markdown-fixer is installed:**
```bash
which markdown-fixer
```

### Hook Running Too Often

If the hook is fixing files you don't want fixed:

**Option 1: Add exclusions**
Edit the hook to skip certain files:
```bash
if [[ "$file" == *"CHANGELOG.md"* ]]; then
    continue
fi
```

**Option 2: Disable the hook**
```bash
mv .claude/hooks/user-prompt-submit.sh .claude/hooks/user-prompt-submit.sh.disabled
```

### Want to See What It's Doing

Enable verbose mode in the hook:
```bash
# Replace this line:
markdown-fixer "$file" --in-place --quiet 2>/dev/null

# With this:
echo "Auto-fixing: $file"
markdown-fixer "$file" --in-place --verbose
```

## Advanced Usage

### Conditional Auto-Fix

Only fix certain files:
```bash
# Only fix README and docs
if [[ "$file" == "README.md" ]] || [[ "$file" == docs/* ]]; then
    markdown-fixer "$file" --in-place --quiet
fi
```

### Pre-Commit Hook

Create a git pre-commit hook instead:
```bash
# .git/hooks/pre-commit
#!/bin/bash
git diff --cached --name-only --diff-filter=ACM | grep '\.md$' | xargs -I {} markdown-fixer {} -i
```

### Notification on Fix

Show a notification when files are fixed:
```bash
if markdown-fixer "$file" --in-place; then
    echo "✓ Fixed: $file"
fi
```

## Best Practices

1. **Commit before bulk operations**: Auto-fix is safe, but commits give you rollback
2. **Test the hook**: Edit a markdown file and verify it works
3. **Monitor initially**: Enable verbose mode to see what's happening
4. **Disable when needed**: For large refactors, disable temporarily
5. **Keep markdown-fixer updated**: `pip install --upgrade markdown-fixer`

## See Also

- [Skill Documentation](../../skill/README.md) - For manual markdown fixing
- [Main README](../../README.md) - Project overview
- Claude Code Hooks Documentation - Official Claude Code docs
