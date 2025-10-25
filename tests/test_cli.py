"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner
from pathlib import Path
from markdown_fixer.cli import main


class TestCLI:
    """Test command-line interface."""

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert '1.0.0' in result.output

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Fix markdown formatting issues' in result.output

    def test_fix_file_in_place(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item\nText")

        runner = CliRunner()
        result = runner.invoke(main, [str(test_file), '--in-place'])

        assert result.exit_code == 0
        assert 'Formatted' in result.output
        content = test_file.read_text()
        assert '\n\n- List item\n\n' in content

    def test_dry_run(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        original_content = "# Header\n- List item\nText"
        test_file.write_text(original_content)

        runner = CliRunner()
        result = runner.invoke(main, [str(test_file), '--dry-run'])

        assert result.exit_code == 0
        # File should not be modified
        assert test_file.read_text() == original_content
        # Output should contain the formatted content
        assert '- List item' in result.output

    def test_output_option(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item\nText")
        output_file = tmp_path / "output.md"

        runner = CliRunner()
        result = runner.invoke(main, [str(test_file), '--output', str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()

    def test_multiple_files_with_output_fails(self, tmp_path):
        # Create test files
        test_file1 = tmp_path / "test1.md"
        test_file2 = tmp_path / "test2.md"
        test_file1.write_text("# Test 1")
        test_file2.write_text("# Test 2")

        runner = CliRunner()
        result = runner.invoke(main, [
            str(test_file1),
            str(test_file2),
            '--output', 'out.md'
        ])

        assert result.exit_code == 1
        assert 'can only be used with a single input file' in result.output

    def test_verbose_mode(self, tmp_path):
        # Create test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item")

        runner = CliRunner()
        result = runner.invoke(main, [str(test_file), '--verbose', '--in-place'])

        assert result.exit_code == 0
        assert 'Processing:' in result.output
