#!/bin/bash
# Auto-fix markdown files after they are edited
# This hook runs after user submits a prompt in Claude Code

# Only run if markdown-fixer is installed
if ! command -v markdown-fixer &> /dev/null; then
    # Silently skip if not installed (don't spam the user)
    exit 0
fi

# Get list of modified markdown files from git (if in a git repo)
if git rev-parse --git-dir > /dev/null 2>&1; then
    # Find modified .md files that are tracked
    modified_files=$(git diff --name-only --diff-filter=M | grep '\.md$')

    if [ -n "$modified_files" ]; then
        # Fix each modified markdown file
        echo "$modified_files" | while read -r file; do
            if [ -f "$file" ]; then
                # Run markdown-fixer silently
                markdown-fixer "$file" --in-place --quiet 2>/dev/null || true
            fi
        done
    fi
else
    # Not in a git repo - check for any .md files in current directory that were recently modified
    find . -maxdepth 2 -name "*.md" -mmin -2 -type f 2>/dev/null | while read -r file; do
        markdown-fixer "$file" --in-place --quiet 2>/dev/null || true
    done
fi

exit 0
