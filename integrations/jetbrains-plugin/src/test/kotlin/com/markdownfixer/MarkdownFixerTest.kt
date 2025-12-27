package com.markdownfixer

import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test

/**
 * Tests for core markdown fixing functionality.
 *
 * These tests mirror the Python tests in tests/test_core.py to ensure
 * feature parity between the CLI and plugin implementations.
 */
class MarkdownFixerTest {

    private lateinit var fixer: MarkdownFixer

    @Before
    fun setUp() {
        fixer = MarkdownFixer()
    }

    // ========== List Formatting Tests ==========

    @Test
    fun testBlankLineBeforeList() {
        val input = """# Header
- Item 1
- Item 2"""

        val expected = """# Header

- Item 1
- Item 2"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testBlankLineAfterList() {
        val input = """- Item 1
- Item 2
Next paragraph"""

        val expected = """- Item 1
- Item 2

Next paragraph"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testBlankLinesBothSides() {
        val input = """# Header
- Item 1
- Item 2
Next paragraph"""

        val expected = """# Header

- Item 1
- Item 2

Next paragraph"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testOrderedList() {
        val input = """Text
1. First
2. Second
More text"""

        val expected = """Text

1. First
2. Second

More text"""

        assertEquals(expected, fixer.fixString(input))
    }

    // ========== Field Metadata Tests ==========

    @Test
    fun testTwoConsecutiveFieldsToBullets() {
        val input = """**Purpose:** Guide
**Status:** Active"""

        val expected = """
- **Purpose:** Guide
- **Status:** Active
"""

        assertEquals(expected.trim(), fixer.fixString(input).trim())
    }

    @Test
    fun testThreeConsecutiveFields() {
        val input = """**Purpose:** Guide
**Status:** Active
**Updated:** 2025-10-12"""

        val expected = """
- **Purpose:** Guide
- **Status:** Active
- **Updated:** 2025-10-12
"""

        assertEquals(expected.trim(), fixer.fixString(input).trim())
    }

    @Test
    fun testSingleFieldNoBullet() {
        val input = """**Purpose:** Single field"""
        val expected = """**Purpose:** Single field"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testFieldsWithBlankLinesAround() {
        val input = """# Section

**Purpose:** Guide
**Status:** Active

More text"""

        val expected = """# Section

- **Purpose:** Guide
- **Status:** Active

More text"""

        assertEquals(expected, fixer.fixString(input))
    }

    // ========== Newline Collapsing Tests ==========

    @Test
    fun testTripleNewlinesCollapsed() {
        val input = """Section 1


Section 2"""

        val expected = """Section 1

Section 2"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testManyNewlinesCollapsed() {
        val input = """Section 1




Section 2"""

        val expected = """Section 1

Section 2"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testDoubleNewlinesPreserved() {
        val input = """Paragraph 1

Paragraph 2"""

        val expected = """Paragraph 1

Paragraph 2"""

        assertEquals(expected, fixer.fixString(input))
    }

    // ========== Code Block Handling Tests ==========

    @Test
    fun testCodeBlockContentUntouched() {
        val input = """Text
```python
def foo():
- not a list
**Key:** not metadata
```
More text"""

        val result = fixer.fixString(input)

        // Code block content should be unchanged
        assert(result.contains("- not a list"))
        assert(result.contains("**Key:** not metadata"))
    }

    @Test
    fun testListBeforeCodeBlock() {
        val input = """- List item
```
code
```
Text"""

        val expected = """- List item

```
code
```

Text"""

        assertEquals(expected, fixer.fixString(input))
    }

    // ========== Edge Cases ==========

    @Test
    fun testEmptyString() {
        assertEquals("", fixer.fixString(""))
    }

    @Test
    fun testOnlyNewlines() {
        val input = "\n\n\n\n"
        val expected = "\n"
        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testNoChangesNeeded() {
        val input = """# Header

- Item 1
- Item 2

Paragraph"""

        // Should return unchanged
        assertEquals(input, fixer.fixString(input))
    }

    @Test
    fun testMixedListTypes() {
        val input = """- Unordered 1
- Unordered 2
1. Ordered 1
2. Ordered 2
Text"""

        // Lists should be treated separately
        val result = fixer.fixString(input)
        assert(result.contains("- Unordered 1"))
        assert(result.contains("1. Ordered 1"))
    }

    // ========== Field Metadata Edge Cases ==========

    @Test
    fun testFieldMetadataColonInsideBold() {
        val input = """**Author:** James
**Status:** Complete"""

        val expected = """
- **Author:** James
- **Status:** Complete
"""

        assertEquals(expected.trim(), fixer.fixString(input).trim())
    }

    @Test
    fun testFieldMetadataColonOutsideBold() {
        val input = """**Author**: James
**Status**: Complete"""

        val expected = """
- **Author:** James
- **Status:** Complete
"""

        assertEquals(expected.trim(), fixer.fixString(input).trim())
    }

    @Test
    fun testFieldMetadataSeparatedByBlankLine() {
        val input = """**Field1:** Value1

**Field2:** Value2"""

        // Should NOT be converted to bullets because they're separated
        val expected = """**Field1:** Value1

**Field2:** Value2"""

        assertEquals(expected, fixer.fixString(input))
    }

    // ========== Table Formatting Tests ==========

    @Test
    fun testSimpleTableFormatting() {
        val input = """| Header 1|Header 2|Header 3|
|---|---|---|
|val1|val2|val3|
|longer value|v2|v3|"""

        val expected = """| Header 1     | Header 2 | Header 3 |
|:-------------|:---------|:---------|
| val1         | val2     | val3     |
| longer value | v2       | v3       |"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testTableWithAlignment() {
        val input = """| Left|Center|Right|
|:---|:---:|---:|
|Text|Text|Text|"""

        val expected = """| Left | Center | Right |
|:-----|:------:|------:|
| Text |  Text  |  Text |"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testTableWithVaryingWidths() {
        val input = """| Short|Medium length|Very long column content here|
|---|---|---|
|A|B|C|"""

        val expected = """| Short | Medium length | Very long column content here |
|:------|:--------------|:------------------------------|
| A     | B             | C                             |"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testTableWithEmoji() {
        val input = """| Feature|Status|Notes|
|---|---|---|
|Tables|✅|Works|
|Emoji 😀|✅|Full support|"""

        val result = fixer.fixString(input)

        // Should format properly (emoji counts as 2 columns width with icu4j)
        assert(result.contains("✅"))
        assert(result.contains("😀"))
        assert(result.contains("|"))
    }

    @Test
    fun testTableWithCjkCharacters() {
        val input = """| Product|Price|
|---|---|
|Coffee|${'$'}3.50|
|咖啡|¥25|"""

        val result = fixer.fixString(input)

        // Should format properly with CJK characters
        assert(result.contains("Coffee"))
        assert(result.contains("咖啡"))
        assert(result.contains("|"))
    }

    @Test
    fun testTableWithEmptyCells() {
        val input = """| Col1|Col2|Col3|
|---|---|---|
|A|B||
|X||Z|"""

        val expected = """| Col1 | Col2 | Col3 |
|:-----|:-----|:-----|
| A    | B    |      |
| X    |      | Z    |"""

        assertEquals(expected, fixer.fixString(input))
    }

    @Test
    fun testMalformedTableMissingCells() {
        val input = """| Col1|Col2|Col3|
|---|---|---|
|A|B|
|X|"""

        // Should pad missing cells with empty
        val result = fixer.fixString(input)

        // Should have three pipes per row
        val lines = result.split('\n')
        for (line in lines) {
            assertEquals(4, line.count { it == '|' })  // 4 pipes = 3 columns
        }
    }

    @Test
    fun testMalformedTableExtraCells() {
        val input = """| A|B|C|
|---|---|---|
|1|2|3|4|5|"""

        // Should truncate extra cells
        val result = fixer.fixString(input)

        // Should have three columns only
        val lines = result.split('\n')
        for (line in lines) {
            assertEquals(4, line.count { it == '|' })  // 4 pipes = 3 columns
        }
    }

    @Test
    fun testTableInCodeBlockUntouched() {
        val input = """Here's a table in code:

```markdown
|Unformatted|Table|
|---|---|
|stays|unformatted|
```

End"""

        val result = fixer.fixString(input)

        // Table inside code block should NOT be formatted
        assert(result.contains("|Unformatted|Table|"))
        assert(result.contains("|stays|unformatted|"))
    }

    @Test
    fun testMultipleTablesInDocument() {
        val input = """# Document

| Table1|Col2|
|---|---|
|A|B|

Some text

| Table2|Col2|Col3|
|---|---|---|
|X|Y|Z|"""

        val result = fixer.fixString(input)

        // Both tables should be formatted
        assert(result.contains("| Table1 |"))
        assert(result.contains("| Table2 |"))
    }

    @Test
    fun testNoTablePresent() {
        val input = """# Regular Document

This has no tables.

Just some text with | a pipe | character."""

        val result = fixer.fixString(input)

        // Should remain unchanged (pipe character alone doesn't make a table)
        assertEquals(input, result)
    }

    @Test
    fun testTableFormattingRealWorld() {
        val input = """# API Documentation

| Endpoint|Method|Description|
|---|:---:|---|
|/users|GET|List all users|
|/users/:id|GET|Get specific user|
|/users|POST|Create new user|"""

        val result = fixer.fixString(input)

        // Should format with proper alignment
        val lines = result.split('\n')
        val tableLines = lines.filter { it.contains('|') }

        // Check header row formatted (index 0)
        assert(tableLines[0].contains("Endpoint"))
        assert(tableLines[0].contains("Method"))
        assert(tableLines[0].contains("Description"))

        // Check center alignment preserved for Method column in delimiter (index 1)
        assert(tableLines[1].contains(":------:") || tableLines[1].contains(":-----:"))
    }

    @Test
    fun testTableWithEscapedPipes() {
        val input = """| Expression|Meaning|
|---|---|
|a \| b|Logical OR|"""

        val result = fixer.fixString(input)

        // Escaped pipe should be preserved
        assert(result.contains("a \\| b"))
    }

    @Test
    fun testTableMixedUnicode() {
        val input = """| Item|Price|Status|
|---|---:|:---:|
|Coffee ☕|${'$'}3.50|✅|
|Tea 🍵|${'$'}2.50|✅|
|水|¥5|✅|"""

        val result = fixer.fixString(input)

        // Should handle mixed ASCII, emoji, and CJK
        assert(result.contains("☕"))
        assert(result.contains("🍵"))
        assert(result.contains("水"))
        assert(result.contains("✅"))
    }
}
