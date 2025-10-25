---
description: Fix all markdown files in the project
---

Fix all markdown files in the current project using markdown-fixer.

Steps:

1. Find all .md files in the project: `find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*"`
2. Show the user the list of files found
3. Ask for confirmation to fix all files
4. If confirmed, run: `markdown-fixer <files> --in-place`
5. Report how many files were fixed

Note: This will modify files in-place. Make sure changes are committed first if needed.
