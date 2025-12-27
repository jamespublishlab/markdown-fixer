#!/bin/bash
# Fix Markdown - Quick Action Script
# Requires markdown-fixer to be installed via pipx or pip
#
# This script should be used in an Automator Quick Action:
# 1. Open Automator
# 2. Create new Quick Action
# 3. Set to receive "files or folders" in "Finder"
# 4. Add "Run Shell Script" action
# 5. Set shell to /bin/bash and pass input as "arguments"
# 6. Paste this script
# 7. Save as "Fix Markdown"

# Set PATH to include common installation locations
export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.local/bin:$PATH"

# Try to find markdown-fixer in multiple locations
if [ -f "$HOME/.local/bin/markdown-fixer" ]; then
    MARKDOWN_FIXER="$HOME/.local/bin/markdown-fixer"
elif [ -f "/opt/homebrew/bin/markdown-fixer" ]; then
    MARKDOWN_FIXER="/opt/homebrew/bin/markdown-fixer"
elif [ -f "/usr/local/bin/markdown-fixer" ]; then
    MARKDOWN_FIXER="/usr/local/bin/markdown-fixer"
elif command -v markdown-fixer &> /dev/null; then
    MARKDOWN_FIXER="markdown-fixer"
else
    # Show error notification
    osascript -e 'display notification "Install from github.com/jamespublishlab/markdown-fixer" with title "Markdown Fixer Not Found" sound name "Basso"' 2>/dev/null || true
    exit 1
fi

# Counter for successfully processed files
count=0
errors=0

# Process each selected file
for f in "$@"; do
    # Check if it's a markdown file
    if [[ "$f" == *.md ]]; then
        if "$MARKDOWN_FIXER" --in-place "$f" 2>/dev/null; then
            ((count++))
        else
            ((errors++))
        fi
    fi
done

# Show completion notification
if [ $count -gt 0 ]; then
    if [ $errors -gt 0 ]; then
        osascript -e "display notification \"Fixed $count file(s), $errors error(s)\" with title \"Markdown Fixer\" sound name \"Glass\"" 2>/dev/null || true
    else
        osascript -e "display notification \"Fixed $count file(s)\" with title \"Markdown Fixer\" sound name \"Glass\"" 2>/dev/null || true
    fi
elif [ $errors -gt 0 ]; then
    osascript -e "display notification \"Failed to fix files\" with title \"Markdown Fixer\" sound name \"Basso\"" 2>/dev/null || true
else
    osascript -e "display notification \"No markdown files selected\" with title \"Markdown Fixer\" sound name \"Basso\"" 2>/dev/null || true
fi

exit 0
