"""Markdown Fixer - Fix common markdown formatting issues."""

from .core import MarkdownFixer, looks_like_markdown
from .__version__ import __version__

__all__ = ["MarkdownFixer", "looks_like_markdown", "__version__"]
