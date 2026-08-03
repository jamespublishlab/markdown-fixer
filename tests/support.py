"""Test-only helper: assert the fixer never silently drops input content."""

import re
from collections import Counter

_WORD_RE = re.compile(r"\w+")


def _word_counts(text: str) -> Counter:
    return Counter(_WORD_RE.findall(text))


def _words_on_removed_horizontal_rules(input_md: str) -> Counter:
    """Words on lines the fixer is designed to delete outright are excused
    from the survives-into-output requirement."""
    from markdown_fixer.core import MarkdownFixer

    removed = Counter()
    for line in input_md.split("\n"):
        if MarkdownFixer._is_horizontal_rule(line):
            removed.update(_word_counts(line))
    return removed


def assert_no_content_lost(input_md: str, output_md: str) -> None:
    """Assert the fixer didn't silently drop any word of input content.

    Every word present in the input must appear in the output at least as
    many times, except for words that appeared only on horizontal-rule
    lines (which the fixer explicitly deletes as a named, intentional
    behavior).
    """
    before = _word_counts(input_md)
    after = _word_counts(output_md)
    excused = _words_on_removed_horizontal_rules(input_md)

    lost = []
    for word, count in before.items():
        allowed_loss = excused.get(word, 0)
        available = after.get(word, 0)
        if available < count - allowed_loss:
            lost.append((word, count, available))

    assert not lost, (
        "Content lost during fix_string(): "
        + ", ".join(f"'{w}' {before_n} -> {after_n}" for w, before_n, after_n in lost)
    )
