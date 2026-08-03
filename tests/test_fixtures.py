"""Golden-file fixture tests: realistic multi-feature documents run through
the fixer and diffed against a hand-reviewed expected output."""

from pathlib import Path

import pytest

from markdown_fixer import MarkdownFixer
from support import assert_no_content_lost

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def discover_fixtures():
    return sorted(p for p in FIXTURES_DIR.iterdir() if p.is_dir())


@pytest.mark.parametrize("fixture_dir", discover_fixtures(), ids=lambda p: p.name)
def test_golden_fixture(fixture_dir):
    input_md = (fixture_dir / "input.md").read_text()
    expected = (fixture_dir / "expected.md").read_text()

    result = MarkdownFixer().fix_string(input_md)

    assert result == expected
    assert_no_content_lost(input_md, result)
