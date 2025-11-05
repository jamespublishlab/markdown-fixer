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
}
