package com.markdownfixer

/**
 * Core markdown formatting logic.
 *
 * Fixes common markdown formatting issues:
 * - Adds proper blank lines around lists
 * - Converts consecutive field-style metadata to bulleted lists
 * - Collapses excessive newlines
 * - Preserves code blocks and blockquotes
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
}
