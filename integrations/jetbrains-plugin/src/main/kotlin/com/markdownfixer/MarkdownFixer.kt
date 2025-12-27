package com.markdownfixer

import com.ibm.icu.lang.UCharacter
import com.ibm.icu.lang.UProperty

/**
 * Core markdown formatting logic.
 *
 * Fixes common markdown formatting issues:
 * - Adds proper blank lines around lists
 * - Converts consecutive field-style metadata to bulleted lists
 * - Collapses excessive newlines
 * - Preserves code blocks and blockquotes
 * - Formats markdown tables with proper alignment
 */
class MarkdownFixer {

    /**
     * Fix markdown content string.
     *
     * @param content Raw markdown content
     * @return Formatted markdown content
     */
    fun fixString(content: String): String {
        val lines = content.split('\n')
        val result = mutableListOf<String>()
        var inCodeBlock = false
        var inList = false
        val fieldMetadataBuffer = mutableListOf<String>()
        var i = 0

        while (i < lines.size) {
            val line = lines[i]

            // Track code blocks (don't process their content)
            if (isCodeFence(line)) {
                // Flush any pending field metadata before code block
                if (fieldMetadataBuffer.isNotEmpty()) {
                    flushFieldMetadata(result, fieldMetadataBuffer, lines, i)
                    fieldMetadataBuffer.clear()
                }

                inCodeBlock = !inCodeBlock
                result.add(line)
                i++
                continue
            }

            // Don't process lines inside code blocks
            if (inCodeBlock) {
                result.add(line)
                i++
                continue
            }

            // Check if this is the start of a table
            if (isTableRow(line) && i + 1 < lines.size && isDelimiterRow(lines[i + 1])) {
                // Flush any pending field metadata before table
                if (fieldMetadataBuffer.isNotEmpty()) {
                    flushFieldMetadata(result, fieldMetadataBuffer, lines, i)
                    fieldMetadataBuffer.clear()
                }

                // Extract and format the entire table
                val (tableLines, tableEndIdx) = extractTable(lines, i)
                val formattedTable = formatTable(tableLines)
                result.addAll(formattedTable)
                i = tableEndIdx + 1
                continue
            }

            // Check if this is field-style metadata
            if (isFieldMetadata(line)) {
                // Extract the field and value - try all patterns
                val stripped = line.trim()

                // Try **Key:** value (colon inside bold)
                var match = Regex("""^\*\*([^*]+):\*\*\s+(.+)$""").find(stripped)
                if (match == null) {
                    // Try **Key**: value (colon outside bold)
                    match = Regex("""^\*\*([^*:]+)\*\*:\s+(.+)$""").find(stripped)
                }
                if (match == null) {
                    // Try **Key**text: value (edge case with text between bold and colon)
                    match = Regex("""^\*\*([^*]+)\*\*[^:]*:\s+(.+)$""").find(stripped)
                }

                if (match != null) {
                    val (field, value) = match.destructured
                    // Normalize to **Key:** value format (colon inside bold)
                    fieldMetadataBuffer.add("**$field:** $value")
                    i++
                    continue
                }
            }

            // If we have buffered field metadata and hit a non-field line, flush it
            if (fieldMetadataBuffer.isNotEmpty() && !isFieldMetadata(line)) {
                flushFieldMetadata(result, fieldMetadataBuffer, lines, i)
                fieldMetadataBuffer.clear()
            }

            // Check if this is a list item
            val isListLine = isListItem(line)

            if (isListLine && !inList) {
                // Starting a list - ensure blank line before
                if (result.isNotEmpty() && result.last().isNotBlank()) {
                    result.add("")
                }
                inList = true
                result.add(line)
            } else if (isListLine && inList) {
                // Continuing a list
                result.add(line)
            } else if (!isListLine && inList) {
                // Ending a list - ensure blank line after
                inList = false
                if (line.isNotBlank()) {  // Only add blank if next line isn't already blank
                    result.add("")
                }
                result.add(line)
            } else {
                // Regular line (not list-related)
                result.add(line)
            }

            i++
        }

        // Flush any remaining field metadata at end of file
        if (fieldMetadataBuffer.isNotEmpty()) {
            flushFieldMetadata(result, fieldMetadataBuffer, emptyList(), lines.size)
        }

        // Join lines and collapse excessive newlines
        var formatted = result.joinToString("\n")

        // Collapse 3+ consecutive newlines to exactly 2 (one blank line)
        formatted = Regex("""\n{3,}""").replace(formatted, "\n\n")

        return formatted
    }

    /**
     * Flush buffered field metadata to result.
     */
    private fun flushFieldMetadata(
        result: MutableList<String>,
        buffer: List<String>,
        lines: List<String>,
        nextLineIdx: Int
    ) {
        // Only convert to bullet list if there are 2+ consecutive field metadata lines
        if (buffer.size >= 2) {
            // Add blank line before if needed
            if (result.isNotEmpty() && result.last().isNotBlank()) {
                result.add("")
            }

            // Add as bulleted list
            buffer.forEach { item ->
                result.add("- $item")
            }

            // Add blank line after
            val nextLine = if (nextLineIdx < lines.size) lines[nextLineIdx] else ""
            if (nextLine.isNotBlank()) {  // Only if next line isn't already blank
                result.add("")
            }
        } else {
            // Single field metadata line - keep as-is (no bullet)
            result.add(buffer[0])
        }
    }

    /**
     * Check if a line is a list item (ordered or unordered).
     */
    private fun isListItem(line: String): Boolean {
        val stripped = line.trimStart()

        // Unordered lists: -, *, +
        if (stripped.startsWith("- ") || stripped.startsWith("* ") || stripped.startsWith("+ ")) {
            return true
        }

        // Ordered lists: 1., 2., etc.
        if (Regex("""^\d+\.\s""").find(stripped) != null) {
            return true
        }

        return false
    }

    /**
     * Check if a line is field-style metadata: **Key:** value or **Key**: value or **Key**text: value
     */
    private fun isFieldMetadata(line: String): Boolean {
        val stripped = line.trim()

        // Match various field metadata patterns:
        // 1. **Key:** value (colon inside bold)
        // 2. **Key**: value (colon outside bold)
        // 3. **Key**text: value (text between bold and colon - edge case)
        return Regex("""^\*\*[^*]+:\*\*\s+.+$""").matches(stripped) ||
               Regex("""^\*\*[^*:]+\*\*:\s+.+$""").matches(stripped) ||
               Regex("""^\*\*[^*]+\*\*[^:]*:\s+.+$""").matches(stripped)
    }

    /**
     * Check if line is a code fence (```... or ~~~...).
     */
    private fun isCodeFence(line: String): Boolean {
        val stripped = line.trim()
        return stripped.startsWith("```") || stripped.startsWith("~~~")
    }

    // ========== Table Formatting Methods ==========

    /**
     * Check if a line contains pipes and looks like a table row.
     */
    private fun isTableRow(line: String): Boolean {
        val stripped = line.trim()
        // Must have at least one pipe (even without leading/trailing pipes)
        // Avoid matching other pipe-like content
        return stripped.contains('|') && !stripped.startsWith('>')
    }

    /**
     * Check if a line is a table delimiter row (contains dashes and pipes).
     */
    private fun isDelimiterRow(line: String): Boolean {
        val stripped = line.trim()
        // Must contain pipes and dashes, and optionally colons for alignment
        // Pattern: |---|--:|:--:|
        return Regex("""^\|?[\s:]*-+[\s:]*(\|[\s:]*-+[\s:]*)+\|?\s*$""").matches(stripped)
    }

    /**
     * Extract a complete table starting from startIdx.
     *
     * Returns Pair of (tableLines, endIndex)
     */
    private fun extractTable(lines: List<String>, startIdx: Int): Pair<List<String>, Int> {
        val tableLines = mutableListOf<String>()
        var i = startIdx

        // Collect all consecutive table rows
        while (i < lines.size && isTableRow(lines[i])) {
            tableLines.add(lines[i])
            i++
        }

        // End index is the last line that was part of the table
        return Pair(tableLines, i - 1)
    }

    /**
     * Parse a table row, splitting on unescaped pipes.
     *
     * Returns list of cell contents with whitespace stripped.
     */
    private fun parseTableRow(line: String): MutableList<String> {
        // Split on pipes that aren't preceded by backslash
        val cells = line.split(Regex("""(?<!\\)\|""")).map { it.trim() }.toMutableList()

        // Remove leading/trailing empty cells (from leading/trailing pipes)
        if (cells.isNotEmpty() && cells[0].isEmpty()) {
            cells.removeAt(0)
        }
        if (cells.isNotEmpty() && cells[cells.size - 1].isEmpty()) {
            cells.removeAt(cells.size - 1)
        }

        return cells
    }

    /**
     * Parse alignment from delimiter row cells.
     *
     * Returns list of 'left', 'center', or 'right' for each column.
     */
    private fun parseAlignments(delimiterRow: List<String>): List<String> {
        return delimiterRow.map { cell ->
            val trimmed = cell.trim()
            when {
                trimmed.startsWith(':') && trimmed.endsWith(':') -> "center"
                trimmed.endsWith(':') -> "right"
                else -> "left"
            }
        }
    }

    /**
     * Calculate display width of text, accounting for Unicode, CJK, and emoji.
     */
    private fun displayWidth(text: String): Int {
        var width = 0
        for (char in text) {
            val eaWidth = UCharacter.getIntPropertyValue(char.code, UProperty.EAST_ASIAN_WIDTH)
            width += when (eaWidth) {
                UCharacter.EastAsianWidth.FULLWIDTH,
                UCharacter.EastAsianWidth.WIDE -> 2
                else -> {
                    // Check if it's an emoji or other wide character
                    if (char.code >= 0x1F300) 2 else 1
                }
            }
        }
        return width
    }

    /**
     * Calculate the maximum display width for each column.
     */
    private fun calculateColumnWidths(rows: List<List<String>>, delimiterIdx: Int): List<Int> {
        if (rows.isEmpty()) return emptyList()

        val numCols = rows[0].size
        val widths = MutableList(numCols) { 0 }

        rows.forEachIndexed { i, row ->
            // Skip delimiter row for content width calculation
            if (i == delimiterIdx) return@forEachIndexed

            row.forEachIndexed { j, cell ->
                if (j < numCols) {
                    widths[j] = maxOf(widths[j], displayWidth(cell))
                }
            }
        }

        // Ensure minimum width of 3 for delimiter
        return widths.map { maxOf(it, 3) }
    }

    /**
     * Format a data row with proper alignment and padding.
     */
    private fun formatTableRow(cells: List<String>, widths: List<Int>, alignments: List<String>): String {
        val formattedCells = mutableListOf<String>()

        cells.forEachIndexed { i, cell ->
            if (i >= widths.size) return@forEachIndexed

            val width = widths[i]
            val align = if (i < alignments.size) alignments[i] else "left"

            // Calculate padding needed
            val cellWidth = displayWidth(cell)
            val paddingNeeded = width - cellWidth

            val formatted = when (align) {
                "left" -> cell + " ".repeat(paddingNeeded)
                "right" -> " ".repeat(paddingNeeded) + cell
                else -> { // center
                    val leftPad = paddingNeeded / 2
                    val rightPad = paddingNeeded - leftPad
                    " ".repeat(leftPad) + cell + " ".repeat(rightPad)
                }
            }

            formattedCells.add(formatted)
        }

        return "| " + formattedCells.joinToString(" | ") + " |"
    }

    /**
     * Format the delimiter row with alignment markers matching column widths.
     */
    private fun formatDelimiterRow(widths: List<Int>, alignments: List<String>): String {
        val delimiters = widths.mapIndexed { i, width ->
            val align = if (i < alignments.size) alignments[i] else "left"

            when (align) {
                "left" -> ":" + "-".repeat(width + 1)  // Add extra dash to account for space
                "right" -> "-".repeat(width + 1) + ":" // Add extra dash to account for space
                else -> ":" + "-".repeat(width) + ":"  // center
            }
        }

        return "|" + delimiters.joinToString("|") + "|"
    }

    /**
     * Format an entire table with proper alignment and column widths.
     */
    private fun formatTable(tableLines: List<String>): List<String> {
        if (tableLines.size < 2) {
            // Not a valid table (need at least header + delimiter)
            return tableLines
        }

        // Parse all rows
        val rows = tableLines.map { parseTableRow(it) }

        // Ensure all rows have the same number of columns (pad with empty cells)
        val numCols = if (rows.isNotEmpty()) rows[0].size else 0
        rows.forEach { row ->
            while (row.size < numCols) {
                row.add("")
            }
            // Truncate extra cells
            if (row.size > numCols) {
                while (row.size > numCols) {
                    row.removeAt(row.size - 1)
                }
            }
        }

        // Parse alignments from delimiter row (index 1)
        val delimiterIdx = 1
        val alignments = parseAlignments(rows[delimiterIdx])

        // Calculate column widths (excluding delimiter)
        val widths = calculateColumnWidths(rows, delimiterIdx)

        // Format each row
        return rows.mapIndexed { i, row ->
            if (i == delimiterIdx) {
                // Format delimiter row
                formatDelimiterRow(widths, alignments)
            } else {
                // Format data row
                formatTableRow(row, widths, alignments)
            }
        }
    }
}
