#!/usr/bin/env python3
"""
Core markdown formatting logic.
"""

import re
from pathlib import Path
from typing import Optional


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
        in_list = False
        field_metadata_buffer = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Track code blocks (don't process their content)
            if self._is_code_fence(line):
                # Flush any pending field metadata before code block
                if field_metadata_buffer:
                    self._flush_field_metadata(result, field_metadata_buffer, lines, i)
                    field_metadata_buffer = []

                in_code_block = not in_code_block
                result.append(line)
                i += 1
                continue

            # Don't process lines inside code blocks
            if in_code_block:
                result.append(line)
                i += 1
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
                if result and result[-1].strip():
                    result.append('')
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
