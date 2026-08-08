#!/usr/bin/env bash
# Build the self-contained markdown-fixer zipapp.
#
# The staged copy is required: src/ also contains markdown_fixer.egg-info/ and
# __pycache__/, which would otherwise be baked into the artifact.
#
# Usage:
#   ./scripts/build-zipapp.sh            # -> dist/markdown-fixer
#   ./scripts/build-zipapp.sh /tmp/out   # -> /tmp/out/markdown-fixer
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$REPO_ROOT/dist}"

STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGE_DIR"' EXIT

cp -R "$REPO_ROOT/src/markdown_fixer" "$STAGE_DIR/"
find "$STAGE_DIR" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
find "$STAGE_DIR" -name '*.pyc' -delete

mkdir -p "$OUT_DIR"
python3 -m zipapp "$STAGE_DIR" \
    -m "markdown_fixer.cli:main" \
    -p "/usr/bin/env python3" \
    -o "$OUT_DIR/markdown-fixer"
chmod +x "$OUT_DIR/markdown-fixer"

echo "Built $OUT_DIR/markdown-fixer"
