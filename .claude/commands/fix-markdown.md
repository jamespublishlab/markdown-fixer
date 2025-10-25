---
description: Fix markdown formatting issues in files
---

Fix markdown formatting issues in the specified file(s) using the markdown-fixer utility.

When invoked:
1. Check if markdown-fixer is installed by running: `which markdown-fixer`
2. If not installed, install it with: `pip install -e .` from the project root
3. Fix the markdown file(s) specified by the user with: `markdown-fixer <file> --in-place`
4. Show the user what was fixed

If no file is specified, ask the user which markdown file(s) they want to fix.

Examples:
- `/fix-markdown README.md` - Fix README.md in place
- `/fix-markdown docs/*.md` - Fix all markdown files in docs/
- `/fix-markdown` - Ask user which files to fix
