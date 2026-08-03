"""Tests for the no-content-lost invariant helper."""

import pytest

from support import assert_no_content_lost


class TestAssertNoContentLost:
    def test_passes_when_nothing_lost(self):
        input_md = "**Purpose:** Guide\n**Status:** Active"
        output_md = "- **Purpose:** Guide\n- **Status:** Active"

        assert_no_content_lost(input_md, output_md)  # should not raise

    def test_raises_when_word_disappears(self):
        input_md = "**Required fix.** Rebase Task 5b on this: the accessor is X."
        output_md = "**Required fix.:** the accessor is X."

        with pytest.raises(AssertionError, match="Rebase"):
            assert_no_content_lost(input_md, output_md)

    def test_excuses_words_only_on_removed_horizontal_rule_lines(self):
        input_md = "Use `___` for underscore emphasis.\n\n___\n\nDone."
        output_md = "Use `___` for underscore emphasis.\n\nDone."

        assert_no_content_lost(input_md, output_md)  # should not raise
