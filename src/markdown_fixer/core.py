#!/usr/bin/env python3
"""
Core markdown formatting logic.
"""

import re
from pathlib import Path
from typing import Optional, List, Tuple

try:
    import wcwidth
    HAS_WCWIDTH = True
except ImportError:
    HAS_WCWIDTH = False


class MarkdownFixer:
    """Fixes common markdown formatting issues."""

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the markdown fixer.

        Args:
            config: Optional configuration dict (reserved for future use)
        """
        self.config = config or {}

    def fix_file(self, filepath: str, in_place: bool = True, output_path: Optional[str] = None) -> str:
        """
        Fix a markdown file.

        Args:
            filepath: Path to the markdown file
            in_place: If True, overwrites the original file
            output_path: If provided and in_place=False, writes to this path

        Returns:
            Path to the output file
        """
        input_path = Path(filepath)
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")

        if not input_path.suffix == '.md':
            # Warning but continue
            pass

        content = input_path.read_text(encoding='utf-8')
        formatted = self.fix_string(content)

        if in_place:
            input_path.write_text(formatted, encoding='utf-8')
            return str(input_path)
        elif output_path:
            output = Path(output_path)
            output.write_text(formatted, encoding='utf-8')
            return str(output)
        else:
            # Create .formatted.md
            output = input_path.with_suffix('.formatted.md')
            output.write_text(formatted, encoding='utf-8')
            return str(output)

    def fix_string(self, content: str) -> str:
        """
        Fix markdown content string.

        Args:
            content: Raw markdown content

        Returns:
            Formatted markdown content
        """
        lines = content.split('\n')
        result = []
        in_code_block = False
        just_exited_block = False  # Track if we just exited a block element
        in_list = False
        field_metadata_buffer = []
        i = 0

        def ensure_blank_before():
            """Add blank line before current element if needed."""
            if result and result[-1].strip():
                result.append('')

        while i < len(lines):
            line = lines[i]

            # Skip horizontal rules (remove them, but maintain spacing)
            if not in_code_block and self._is_horizontal_rule(line):
                # Add a blank line if we're not already at a blank line
                # This maintains document structure when rules are removed
                if result and result[-1].strip():
                    result.append('')
                i += 1
                continue

            # Track code blocks (don't process their content)
            if self._is_code_fence(line):
                # Flush any pending field metadata before code block
                if field_metadata_buffer:
                    self._flush_field_metadata(result, field_metadata_buffer, lines, i)
                    field_metadata_buffer = []

                # End list if we were in one
                if in_list:
                    in_list = False

                if not in_code_block:
                    # Opening code fence - ensure blank line before
                    ensure_blank_before()
                else:
                    # Closing code fence - mark that we just exited a block
                    just_exited_block = True

                in_code_block = not in_code_block
                result.append(line)
                i += 1
                continue

            # Don't process lines inside code blocks
            if in_code_block:
                result.append(line)
                i += 1
                continue

            # Add blank line after block element if followed by content
            if just_exited_block:
                just_exited_block = False
                if line.strip():  # Non-blank line after block
                    result.append('')

            # Check if this is a heading
            if self._is_heading(line):
                # Flush any pending field metadata
                if field_metadata_buffer:
                    self._flush_field_metadata(result, field_metadata_buffer, lines, i)
                    field_metadata_buffer = []

                # End list if we were in one
                if in_list:
                    in_list = False

                # Ensure blank line before heading
                ensure_blank_before()
                result.append(line)
                # Mark that next content needs blank line before it
                just_exited_block = True
                i += 1
                continue

            # Check if this is the start of a table
            if self._is_table_row(line) and i + 1 < len(lines) and self._is_delimiter_row(lines[i + 1]):
                # Flush any pending field metadata before table
                if field_metadata_buffer:
                    self._flush_field_metadata(result, field_metadata_buffer, lines, i)
                    field_metadata_buffer = []

                # End list if we were in one
                if in_list:
                    in_list = False

                # Ensure blank line before table
                ensure_blank_before()

                # Extract and format the entire table
                table_lines, table_end_idx = self._extract_table(lines, i)
                formatted_table = self._format_table(table_lines)
                result.extend(formatted_table)
                # Mark that next content needs blank line before it
                just_exited_block = True
                i = table_end_idx + 1
                continue

            # Check if this is field-style metadata
            if self._is_field_metadata(line):
                # Extract the field and value - try all patterns
                stripped = line.strip()
                # Try **Key:** value (colon inside bold)
                match = re.match(r'^\*\*([^*]+):\*\*\s+(.+)$', stripped)
                if not match:
                    # Try **Key**: value (colon outside bold)
                    match = re.match(r'^\*\*([^*:]+)\*\*:\s+(.+)$', stripped)
                if not match:
                    # Try **Key**text: value (edge case with text between bold and colon)
                    match = re.match(r'^\*\*([^*]+)\*\*[^:]*:\s+(.+)$', stripped)

                if match:
                    field, value = match.groups()
                    # Normalize to **Key:** value format (colon inside bold)
                    field_metadata_buffer.append(f'**{field}:** {value}')
                    i += 1
                    continue

            # If we have buffered field metadata and hit a non-field line, flush it
            if field_metadata_buffer and not self._is_field_metadata(line):
                self._flush_field_metadata(result, field_metadata_buffer, lines, i)
                field_metadata_buffer = []

            # Check if this is a list item
            is_list_line = self._is_list_item(line)

            if is_list_line and not in_list:
                # Starting a list - ensure blank line before
                ensure_blank_before()
                in_list = True
                result.append(line)

            elif is_list_line and in_list:
                # Continuing a list
                result.append(line)

            elif not is_list_line and in_list:
                # Ending a list - ensure blank line after
                in_list = False
                if line.strip():  # Only add blank if next line isn't already blank
                    result.append('')
                result.append(line)

            else:
                # Regular line (not list-related)
                result.append(line)

            i += 1

        # Flush any remaining field metadata at end of file
        if field_metadata_buffer:
            self._flush_field_metadata(result, field_metadata_buffer, [], len(lines))

        # Join lines and collapse excessive newlines
        formatted = '\n'.join(result)

        # Collapse 3+ consecutive newlines to exactly 2 (one blank line)
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)

        return formatted

    def _flush_field_metadata(self, result: list, buffer: list, lines: list, next_line_idx: int):
        """Flush buffered field metadata to result."""
        # Only convert to bullet list if there are 2+ consecutive field metadata lines
        if len(buffer) >= 2:
            # Add blank line before if needed
            if result and result[-1].strip():
                result.append('')

            # Add as bulleted list
            result.extend([f'- {item}' for item in buffer])

            # Add blank line after
            next_line = lines[next_line_idx] if next_line_idx < len(lines) else ''
            if next_line.strip():  # Only if next line isn't already blank
                result.append('')
        else:
            # Single field metadata line - keep as-is (no bullet)
            result.append(buffer[0])

    @staticmethod
    def _is_list_item(line: str) -> bool:
        """Check if a line is a list item (ordered or unordered)."""
        stripped = line.lstrip()
        # Unordered lists: -, *, +
        if stripped.startswith(('- ', '* ', '+ ')):
            return True
        # Ordered lists: 1., 2., etc.
        if re.match(r'^\d+\.\s', stripped):
            return True
        return False

    @staticmethod
    def _is_field_metadata(line: str) -> bool:
        """Check if a line is field-style metadata: **Key:** value or **Key**: value or **Key**text: value"""
        stripped = line.strip()
        # Match various field metadata patterns:
        # 1. **Key:** value (colon inside bold)
        # 2. **Key**: value (colon outside bold)
        # 3. **Key**text: value (text between bold and colon - edge case)
        return bool(re.match(r'^\*\*[^*]+:\*\*\s+.+$', stripped) or
                   re.match(r'^\*\*[^*:]+\*\*:\s+.+$', stripped) or
                   re.match(r'^\*\*[^*]+\*\*[^:]*:\s+.+$', stripped))

    @staticmethod
    def _is_code_fence(line: str) -> bool:
        """Check if line is a code fence (```...)."""
        stripped = line.strip()
        return stripped.startswith('```') or stripped.startswith('~~~')

    @staticmethod
    def _is_heading(line: str) -> bool:
        """Check if line is a markdown heading (# Header)."""
        stripped = line.strip()
        # Match # followed by space, or ## followed by space, etc.
        return bool(re.match(r'^#{1,6}\s+\S', stripped))

    @staticmethod
    def _is_horizontal_rule(line: str) -> bool:
        """Check if line is a horizontal rule (---, ***, ___ with 3+ chars)."""
        stripped = line.strip()
        # Match lines that are only dashes, asterisks, or underscores (3 or more)
        # May have spaces between them
        if len(stripped) < 3:
            return False
        # Remove spaces and check if all remaining chars are the same rule char
        no_spaces = stripped.replace(' ', '')
        if len(no_spaces) < 3:
            return False
        return (all(c == '-' for c in no_spaces) or
                all(c == '*' for c in no_spaces) or
                all(c == '_' for c in no_spaces))

    # ========== Table Formatting Methods ==========

    @staticmethod
    def _is_table_row(line: str) -> bool:
        """Check if a line contains pipes and looks like a table row."""
        stripped = line.strip()
        # Must have at least one pipe (even without leading/trailing pipes)
        # Avoid matching other pipe-like content
        return '|' in stripped and not stripped.startswith('>')

    @staticmethod
    def _is_delimiter_row(line: str) -> bool:
        """Check if a line is a table delimiter row (contains dashes and pipes)."""
        stripped = line.strip()
        # Must contain pipes and dashes, and optionally colons for alignment
        # Pattern: |---|--:|:--:|
        return bool(re.match(r'^\|?[\s:]*-+[\s:]*(\|[\s:]*-+[\s:]*)+\|?\s*$', stripped))

    def _extract_table(self, lines: List[str], start_idx: int) -> Tuple[List[str], int]:
        """
        Extract a complete table starting from start_idx.

        Returns:
            Tuple of (table_lines, end_index)
        """
        table_lines = []
        i = start_idx

        # Collect all consecutive table rows
        while i < len(lines) and self._is_table_row(lines[i]):
            table_lines.append(lines[i])
            i += 1

        # End index is the last line that was part of the table
        return table_lines, i - 1

    def _parse_table_row(self, line: str) -> List[str]:
        """
        Parse a table row, splitting on unescaped pipes.

        Returns list of cell contents with whitespace stripped.
        """
        # Split on pipes that aren't preceded by backslash
        cells = re.split(r'(?<!\\)\|', line)

        # Strip whitespace from each cell
        cells = [cell.strip() for cell in cells]

        # Remove leading/trailing empty cells (from leading/trailing pipes)
        if cells and not cells[0]:
            cells = cells[1:]
        if cells and not cells[-1]:
            cells = cells[:-1]

        return cells

    def _parse_alignments(self, delimiter_row: List[str]) -> List[str]:
        """
        Parse alignment from delimiter row cells.

        Returns list of 'left', 'center', or 'right' for each column.
        """
        alignments = []
        for cell in delimiter_row:
            cell = cell.strip()
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')
        return alignments

    def _display_width(self, text: str) -> int:
        """
        Calculate display width of text, accounting for Unicode, CJK, and emoji.
        """
        if HAS_WCWIDTH:
            # Use wcwidth for accurate Unicode width calculation
            return sum(max(wcwidth.wcwidth(char), 0) for char in text)
        else:
            # Fallback: simple length (ASCII-only)
            return len(text)

    def _calculate_column_widths(self, rows: List[List[str]], delimiter_idx: int) -> List[int]:
        """
        Calculate the maximum display width for each column.

        Args:
            rows: All table rows (including delimiter)
            delimiter_idx: Index of delimiter row (usually 1)

        Returns:
            List of column widths
        """
        if not rows:
            return []

        num_cols = len(rows[0])
        widths = [0] * num_cols

        for i, row in enumerate(rows):
            # Ensure row has enough cells (pad with empty if needed)
            while len(row) < num_cols:
                row.append('')

            # Skip delimiter row for content width calculation
            if i == delimiter_idx:
                continue

            for j in range(num_cols):
                if j < len(row):
                    widths[j] = max(widths[j], self._display_width(row[j]))

        # Ensure minimum width of 3 for delimiter
        widths = [max(w, 3) for w in widths]

        return widths

    def _format_table_row(self, cells: List[str], widths: List[int], alignments: List[str]) -> str:
        """
        Format a data row with proper alignment and padding.
        """
        formatted_cells = []

        for i, cell in enumerate(cells):
            if i >= len(widths):
                break

            width = widths[i]
            align = alignments[i] if i < len(alignments) else 'left'

            # Calculate padding needed
            cell_width = self._display_width(cell)
            padding_needed = width - cell_width

            if align == 'left':
                formatted = cell + ' ' * padding_needed
            elif align == 'right':
                formatted = ' ' * padding_needed + cell
            else:  # center
                left_pad = padding_needed // 2
                right_pad = padding_needed - left_pad
                formatted = ' ' * left_pad + cell + ' ' * right_pad

            formatted_cells.append(formatted)

        return '| ' + ' | '.join(formatted_cells) + ' |'

    def _format_delimiter_row(self, widths: List[int], alignments: List[str]) -> str:
        """
        Format the delimiter row with alignment markers matching column widths.
        """
        delimiters = []

        for i, width in enumerate(widths):
            align = alignments[i] if i < len(alignments) else 'left'

            if align == 'left':
                delim = ':' + '-' * (width + 1)  # Add extra dash to account for space
            elif align == 'right':
                delim = '-' * (width + 1) + ':'  # Add extra dash to account for space
            else:  # center
                delim = ':' + '-' * width + ':'

            delimiters.append(delim)

        return '|' + '|'.join(delimiters) + '|'

    def _format_table(self, table_lines: List[str]) -> List[str]:
        """
        Format an entire table with proper alignment and column widths.

        Args:
            table_lines: List of raw table row strings

        Returns:
            List of formatted table row strings
        """
        if len(table_lines) < 2:
            # Not a valid table (need at least header + delimiter)
            return table_lines

        # Parse all rows
        rows = [self._parse_table_row(line) for line in table_lines]

        # Ensure all rows have the same number of columns (pad with empty cells)
        num_cols = len(rows[0]) if rows else 0
        for row in rows:
            while len(row) < num_cols:
                row.append('')
            # Truncate extra cells
            if len(row) > num_cols:
                row[:] = row[:num_cols]

        # Parse alignments from delimiter row (index 1)
        delimiter_idx = 1
        alignments = self._parse_alignments(rows[delimiter_idx])

        # Calculate column widths (excluding delimiter)
        widths = self._calculate_column_widths(rows, delimiter_idx)

        # Format each row
        formatted = []
        for i, row in enumerate(rows):
            if i == delimiter_idx:
                # Format delimiter row
                formatted.append(self._format_delimiter_row(widths, alignments))
            else:
                # Format data row
                formatted.append(self._format_table_row(row, widths, alignments))

        return formatted
