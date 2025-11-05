"""Tests for core markdown fixing functionality."""

import pytest
from markdown_fixer import MarkdownFixer


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

        expected = """- List item

```
code
```

Text"""

        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)
        # Should have blank line after list and before text
        assert result.count('\n\n') >= 2


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
        lines = result.split('\n')
        for line in lines:
            assert line.count('|') == 4  # 4 pipes = 3 columns

    def test_malformed_table_extra_cells(self):
        input_md = """| A|B|C|
|---|---|---|
|1|2|3|4|5|"""

        # Should truncate extra cells
        fixer = MarkdownFixer()
        result = fixer.fix_string(input_md)

        # Should have three columns only
        lines = result.split('\n')
        for line in lines:
            assert line.count('|') == 4  # 4 pipes = 3 columns

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
        lines = result.split('\n')
        table_lines = [l for l in lines if '|' in l]

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
        assert result_path.endswith('.formatted.md')
        assert (tmp_path / "test.formatted.md").exists()

    def test_fix_file_custom_output(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item")

        output_file = tmp_path / "output.md"

        fixer = MarkdownFixer()
        result_path = fixer.fix_file(
            str(test_file),
            in_place=False,
            output_path=str(output_file)
        )

        assert result_path == str(output_file)
        assert output_file.exists()
