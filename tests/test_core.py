"""Tests for core markdown fixing functionality."""

from markdown_fixer import MarkdownFixer, looks_like_markdown


class TestLooksLikeMarkdown:
    """Test heuristic markdown content detection."""

    def test_empty_content_returns_false(self):
        assert looks_like_markdown("") is False

    def test_short_content_returns_false(self):
        assert looks_like_markdown("Hello") is False

    def test_plain_text_returns_false(self):
        content = "This is just plain text without any markdown formatting."
        assert looks_like_markdown(content) is False

    def test_header_only_returns_false(self):
        """Single indicator is below default threshold of 2."""
        content = "# Just a header"
        assert looks_like_markdown(content) is False

    def test_header_with_list_returns_true(self):
        content = """# Header
- List item"""
        assert looks_like_markdown(content) is True

    def test_frontmatter_with_header_returns_true(self):
        content = """---
title: Test
---
# Header"""
        assert looks_like_markdown(content) is True

    def test_bold_and_link_returns_true(self):
        content = "This has **bold text** and a [link](http://example.com)."
        assert looks_like_markdown(content) is True

    def test_code_block_with_header_returns_true(self):
        content = """# Code Example
```python
print("hello")
```"""
        assert looks_like_markdown(content) is True

    def test_ordered_list_with_header_returns_true(self):
        content = """# Steps
1. First step
2. Second step"""
        assert looks_like_markdown(content) is True

    def test_blockquote_with_list_returns_true(self):
        content = """> Important note
- Item 1"""
        assert looks_like_markdown(content) is True

    def test_wiki_link_with_header_returns_true(self):
        content = """# My Note
See also [[Other Note]]"""
        assert looks_like_markdown(content) is True

    def test_threshold_parameter(self):
        """Test custom threshold parameter."""
        content = "# Header with enough characters"  # Only one indicator

        # With threshold=1, should return True
        assert looks_like_markdown(content, threshold=1) is True

        # With threshold=2 (default), should return False
        assert looks_like_markdown(content, threshold=2) is False

    def test_code_content_returns_false(self):
        """Python code without markdown features should return False."""
        content = """def hello():
    print("Hello, world!")
    return True"""
        assert looks_like_markdown(content) is False

    def test_json_content_returns_false(self):
        """JSON content should return False."""
        content = '{"name": "test", "value": 123}'
        assert looks_like_markdown(content) is False

    def test_typical_obsidian_note_returns_true(self):
        """Typical Obsidian note with frontmatter and wiki-links."""
        content = """---
tags: [test]
---
# My Note

This links to [[Another Note]] and has a **key point**.

- Item 1
- Item 2"""
        assert looks_like_markdown(content) is True


class TestHeadingFormatting:
    """Test blank lines around headings."""

    def test_blank_line_before_heading(self):
        input_md = """Some text
# Header"""

        expected = """Some text

# Header"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_blank_line_after_heading(self):
        input_md = """# Header
Some text"""

        expected = """# Header

Some text"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_blank_lines_both_sides_of_heading(self):
        input_md = """First paragraph
## Section
Content here"""

        expected = """First paragraph

## Section

Content here"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_heading_at_start_no_blank_before(self):
        """First line heading should not have blank line before."""
        input_md = """# Title
Some text"""

        expected = """# Title

Some text"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_multiple_headings(self):
        input_md = """# Title
Intro text
## Section 1
Content 1
## Section 2
Content 2"""

        expected = """# Title

Intro text

## Section 1

Content 1

## Section 2

Content 2"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected


class TestHorizontalRuleRemoval:
    """Test removal of horizontal rules."""

    def test_remove_triple_dash(self):
        input_md = """First section
---
Second section"""

        expected = """First section

Second section"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_remove_many_dashes(self):
        input_md = """First
----------
Second"""

        expected = """First

Second"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_remove_asterisk_rule(self):
        input_md = """First
***
Second"""

        expected = """First

Second"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_remove_underscore_rule(self):
        input_md = """First
___
Second"""

        expected = """First

Second"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_remove_spaced_rule(self):
        input_md = """First
- - -
Second"""

        expected = """First

Second"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_preserve_dashes_in_code_block(self):
        """Horizontal rules inside code blocks should not be removed."""
        input_md = """```
---
```"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert "---" in result

    def test_dont_remove_list_item(self):
        """A line starting with dash and space is a list item, not a rule."""
        input_md = """- Item 1
- Item 2"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert "- Item 1" in result
        assert "- Item 2" in result


class TestListFormatting:
    """Test blank lines around lists."""

    def test_blank_line_before_list(self):
        input_md = """# Header
- Item 1
- Item 2"""

        expected = """# Header

- Item 1
- Item 2"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_blank_line_after_list(self):
        input_md = """- Item 1
- Item 2
Next paragraph"""

        expected = """- Item 1
- Item 2

Next paragraph"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_blank_lines_both_sides(self):
        input_md = """# Header
- Item 1
- Item 2
Next paragraph"""

        expected = """# Header

- Item 1
- Item 2

Next paragraph"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_ordered_list(self):
        input_md = """Text
1. First
2. Second
More text"""

        expected = """Text

1. First
2. Second

More text"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected


class TestFieldMetadata:
    """Test field metadata conversion."""

    def test_two_consecutive_fields_to_bullets(self):
        input_md = """**Purpose:** Guide
**Status:** Active"""

        expected = """
- **Purpose:** Guide
- **Status:** Active
"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md).strip()
        assert result == expected.strip()

    def test_three_consecutive_fields(self):
        input_md = """**Purpose:** Guide
**Status:** Active
**Updated:** 2025-10-12"""

        expected = """
- **Purpose:** Guide
- **Status:** Active
- **Updated:** 2025-10-12
"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md).strip()
        assert result == expected.strip()

    def test_single_field_no_bullet(self):
        input_md = """**Purpose:** Single field"""

        expected = """**Purpose:** Single field"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_fields_with_blank_lines_around(self):
        input_md = """# Section

**Purpose:** Guide
**Status:** Active

More text"""

        expected = """# Section

- **Purpose:** Guide
- **Status:** Active

More text"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected


class TestNewlineCollapsing:
    """Test excessive newline removal."""

    def test_triple_newlines_collapsed(self):
        input_md = """Section 1


Section 2"""

        expected = """Section 1

Section 2"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_many_newlines_collapsed(self):
        input_md = """Section 1




Section 2"""

        expected = """Section 1

Section 2"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_double_newlines_preserved(self):
        input_md = """Paragraph 1

Paragraph 2"""

        expected = """Paragraph 1

Paragraph 2"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected


class TestCodeBlockHandling:
    """Test that code blocks are never modified."""

    def test_code_block_content_untouched(self):
        input_md = """Text
```python
def foo():
- not a list
**Key:** not metadata
```
More text"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Code block content should be unchanged
        assert "- not a list" in result
        assert "**Key:** not metadata" in result

    def test_list_before_code_block(self):
        input_md = """- List item
```
code
```
Text"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        # Should have blank line after list and before text
        assert result.count("\n\n") >= 2


class TestBlockquoteHandling:
    """Test that blockquotes are handled correctly."""

    def test_blockquote_content_not_converted(self):
        """Field-style content in blockquotes should not be converted to lists."""
        input_md = """> **Note:** This is a callout
> **Warning:** Another callout"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Content should remain as blockquotes, not converted to bullets
        assert "> **Note:**" in result
        assert "> **Warning:**" in result
        # Should NOT be converted to bullet lists
        assert "- **Note:**" not in result

    def test_list_before_blockquote(self):
        """Ensure blank line between list and blockquote."""
        input_md = """- List item
> Blockquote"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should have blank line between list and blockquote
        assert "- List item\n\n>" in result

    def test_blockquote_before_list(self):
        """Blockquote followed by list should work correctly."""
        input_md = """> Quote text
- List item"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should have blank line between blockquote and list
        assert "> Quote text\n\n- List item" in result


class TestImageFormatting:
    """Test blank lines around standalone images."""

    def test_blank_lines_around_markdown_image(self):
        input_md = "Text before\n![alt](image.png)\nText after"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert "Text before\n\n![alt](image.png)\n\nText after" == result

    def test_blank_lines_around_wiki_image(self):
        input_md = "Text before\n![[screenshot.png]]\nText after"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert "Text before\n\n![[screenshot.png]]\n\nText after" == result

    def test_inline_image_not_affected(self):
        input_md = "Text with ![alt](img.png) inline"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert result == input_md

    def test_image_in_list_not_standalone(self):
        input_md = "- ![img](x.png)\n- item"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert "- ![img](x.png)\n- item" == result


class TestFrontmatterPreservation:
    """Test YAML frontmatter is preserved (e.g. Obsidian notes)."""

    def test_obsidian_frontmatter_preserved(self):
        input_md = """---
title: My Note
tags: [project, active]
date: 2026-03-20
---

# My Note

Some content here."""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert result.startswith("---\ntitle: My Note")
        assert "---\n\n# My Note" in result

    def test_frontmatter_with_formatting_fixes(self):
        input_md = """---
title: Test
---

# Header
**Key:** value1
**Key2:** value2
Some text
- item 1
- item 2
More text"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert result.startswith("---\ntitle: Test\n---")
        assert "- **Key:**" in result
        assert "\n\n- item 1" in result

    def test_no_frontmatter_unchanged(self):
        input_md = "# Hello\n\nSome text"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert result == input_md

    def test_empty_frontmatter(self):
        input_md = "---\n---\n\n# Hello"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert result.startswith("---\n---")

    def test_unclosed_frontmatter_not_treated_as_frontmatter(self):
        """A --- without a closing --- should be treated as a horizontal rule."""
        input_md = "---\nJust text"
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        assert not result.startswith("---")


class TestComplexCombinations:
    """Test realistic complex scenarios."""

    def test_llm_generated_document(self):
        input_md = """# Documentation Guide
**Purpose:** Guide for writing docs
**Status:** Active
**Updated:** 2025-10-12

This document provides guidelines.
- Write clearly
- Use examples
- Be concise
The following sections cover:


## Best Practices
Follow these rules:
1. Keep it simple
2. Be consistent
3. Test examples
End of section."""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should have converted field metadata to bullets
        assert "- **Purpose:**" in result
        assert "- **Status:**" in result
        assert "- **Updated:**" in result

        # Should have blank lines around lists
        assert "\n- Write clearly\n" in result or "guidelines.\n\n- Write clearly" in result
        assert "\n1. Keep it simple\n" in result or "rules:\n\n1. Keep it simple" in result

        # Should have collapsed triple newlines
        assert "\n\n\n" not in result


class TestTableFormatting:
    """Test markdown table formatting."""

    def test_simple_table_formatting(self):
        input_md = """| Header 1|Header 2|Header 3|
|---|---|---|
|val1|val2|val3|
|longer value|v2|v3|"""

        expected = """| Header 1     | Header 2 | Header 3 |
|:-------------|:---------|:---------|
| val1         | val2     | val3     |
| longer value | v2       | v3       |"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_table_with_alignment(self):
        input_md = """| Left|Center|Right|
|:---|:---:|---:|
|Text|Text|Text|"""

        expected = """| Left | Center | Right |
|:-----|:------:|------:|
| Text |  Text  |  Text |"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_table_with_varying_widths(self):
        input_md = """| Short|Medium length|Very long column content here|
|---|---|---|
|A|B|C|"""

        expected = """| Short | Medium length | Very long column content here |
|:------|:--------------|:------------------------------|
| A     | B             | C                             |"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_table_with_emoji(self):
        input_md = """| Feature|Status|Notes|
|---|---|---|
|Tables|✅|Works|
|Emoji 😀|✅|Full support|"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should format properly (emoji counts as 2 columns width with wcwidth)
        assert "✅" in result
        assert "😀" in result
        assert "|" in result

    def test_table_with_cjk_characters(self):
        input_md = """| Product|Price|
|---|---|
|Coffee|$3.50|
|咖啡|¥25|"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should format properly with CJK characters
        assert "Coffee" in result
        assert "咖啡" in result
        assert "|" in result

    def test_table_with_empty_cells(self):
        input_md = """| Col1|Col2|Col3|
|---|---|---|
|A|B||
|X||Z|"""

        expected = """| Col1 | Col2 | Col3 |
|:-----|:-----|:-----|
| A    | B    |      |
| X    |      | Z    |"""

        fixer = MarkdownFixer()
        assert fixer.fix_string(input_md) == expected

    def test_malformed_table_missing_cells(self):
        input_md = """| Col1|Col2|Col3|
|---|---|---|
|A|B|
|X|"""

        # Should pad missing cells with empty
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should have three pipes per row
        lines = result.split("\n")
        for line in lines:
            assert line.count("|") == 4  # 4 pipes = 3 columns

    def test_malformed_table_extra_cells(self):
        input_md = """| A|B|C|
|---|---|---|
|1|2|3|4|5|"""

        # Should truncate extra cells
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should have three columns only
        lines = result.split("\n")
        for line in lines:
            assert line.count("|") == 4  # 4 pipes = 3 columns

    def test_table_in_code_block_untouched(self):
        input_md = """Here's a table in code:

```markdown
|Unformatted|Table|
|---|---|
|stays|unformatted|
```

End"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Table inside code block should NOT be formatted
        assert "|Unformatted|Table|" in result
        assert "|stays|unformatted|" in result

    def test_multiple_tables_in_document(self):
        input_md = """# Document

| Table1|Col2|
|---|---|
|A|B|

Some text

| Table2|Col2|Col3|
|---|---|---|
|X|Y|Z|"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Both tables should be formatted
        assert "| Table1 |" in result
        assert "| Table2 |" in result

    def test_no_table_present(self):
        input_md = """# Regular Document

This has no tables.

Just some text with | a pipe | character."""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should remain unchanged (pipe character alone doesn't make a table)
        assert result == input_md

    def test_table_formatting_real_world(self):
        input_md = """# API Documentation

| Endpoint|Method|Description|
|---|:---:|---|
|/users|GET|List all users|
|/users/:id|GET|Get specific user|
|/users|POST|Create new user|"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should format with proper alignment
        lines = result.split("\n")
        table_lines = [line for line in lines if "|" in line]

        # Check header row formatted (index 0)
        assert "Endpoint" in table_lines[0]
        assert "Method" in table_lines[0]
        assert "Description" in table_lines[0]

        # Check center alignment preserved for Method column in delimiter (index 1)
        assert ":------:" in table_lines[1] or ":-----:" in table_lines[1]

    def test_table_with_escaped_pipes(self):
        input_md = r"""| Expression|Meaning|
|---|---|
|a \| b|Logical OR|"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Escaped pipe should be preserved
        assert r"a \| b" in result

    def test_table_mixed_unicode(self):
        input_md = """| Item|Price|Status|
|---|---:|:---:|
|Coffee ☕|$3.50|✅|
|Tea 🍵|$2.50|✅|
|水|¥5|✅|"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should handle mixed ASCII, emoji, and CJK
        assert "☕" in result
        assert "🍵" in result
        assert "水" in result
        assert "✅" in result


class TestFileOperations:
    """Test file reading and writing."""

    def test_fix_file_in_place(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item\nText")

        fixer = MarkdownFixer()
        result_path = fixer.fix_file(str(test_file), in_place=True)

        assert result_path == str(test_file)
        content = test_file.read_text()
        assert "\n\n- List item\n\n" in content

    def test_fix_file_new_output(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item")

        fixer = MarkdownFixer()
        result_path = fixer.fix_file(str(test_file), in_place=False)

        # Should create .formatted.md file
        assert result_path.endswith(".formatted.md")
        assert (tmp_path / "test.formatted.md").exists()

    def test_fix_file_custom_output(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item")

        output_file = tmp_path / "output.md"

        fixer = MarkdownFixer()
        result_path = fixer.fix_file(str(test_file), in_place=False, output_path=str(output_file))

        assert result_path == str(output_file)
        assert output_file.exists()
