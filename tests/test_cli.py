"""Tests for CLI functionality."""

import pytest

from markdown_fixer.__version__ import __version__
from markdown_fixer.cli import main


def run_cli(argv):
    """Invoke the CLI and return its exit code.

    main() always exits via sys.exit(), so every call raises SystemExit.
    SystemExit.code is None when the code was 0.
    """
    with pytest.raises(SystemExit) as excinfo:
        main(argv)
    code = excinfo.value.code
    return 0 if code is None else code


class TestCLI:
    """Test command-line interface."""

    def test_version(self, capsys):
        code = run_cli(["--version"])
        out = capsys.readouterr().out
        assert code == 0
        assert __version__ in out

    def test_help(self, capsys):
        code = run_cli(["--help"])
        out = capsys.readouterr().out
        assert code == 0
        assert "Fix markdown formatting issues" in out

    def test_fix_file_in_place(self, tmp_path, capsys):
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item\nText")

        code = run_cli([str(test_file), "--in-place"])
        out = capsys.readouterr().out

        assert code == 0
        assert "Formatted" in out
        assert "\n\n- List item\n\n" in test_file.read_text()

    def test_dry_run(self, tmp_path, capsys):
        test_file = tmp_path / "test.md"
        original_content = "# Header\n- List item\nText"
        test_file.write_text(original_content)

        code = run_cli([str(test_file), "--dry-run"])
        out = capsys.readouterr().out

        assert code == 0
        assert test_file.read_text() == original_content
        assert "- List item" in out

    def test_output_option(self, tmp_path):
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item\nText")
        output_file = tmp_path / "output.md"

        code = run_cli([str(test_file), "--output", str(output_file)])

        assert code == 0
        assert output_file.exists()

    def test_multiple_files_with_output_fails(self, tmp_path, capsys):
        test_file1 = tmp_path / "test1.md"
        test_file2 = tmp_path / "test2.md"
        test_file1.write_text("# Test 1")
        test_file2.write_text("# Test 2")

        code = run_cli([str(test_file1), str(test_file2), "--output", "out.md"])
        err = capsys.readouterr().err

        assert code == 1
        assert "can only be used with a single input file" in err

    def test_verbose_mode(self, tmp_path, capsys):
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item")

        code = run_cli([str(test_file), "--verbose", "--in-place"])
        out = capsys.readouterr().out

        assert code == 0
        assert "Processing:" in out

    def test_missing_file_errors(self, tmp_path, capsys):
        """click.Path(exists=True) gave this for free; argparse does not.

        --dry-run is load-bearing: without it, core.py's own FileNotFoundError
        satisfies the assertion even when the cli.py check is absent.
        """
        code = run_cli([str(tmp_path / "does-not-exist.md"), "--dry-run"])
        err = capsys.readouterr().err

        assert code == 1
        assert "not found" in err.lower()

    def test_multiple_files_fail_fast_before_any_are_modified(self, tmp_path, capsys):
        """A missing file aborts the run before earlier files are touched."""
        good = tmp_path / "good.md"
        original = "# Header\n- List item\nText"
        good.write_text(original)

        code = run_cli([str(good), str(tmp_path / "missing.md"), "--in-place"])
        err = capsys.readouterr().err

        assert code == 1
        assert "not found" in err.lower()
        assert good.read_text() == original, "earlier file was modified before the run aborted"


class TestReservedWordDispatch:
    """`hook`, `mcp-server`, and `doctor` are reserved first words."""

    def test_hook_dispatches_instead_of_treating_it_as_a_file(self, tmp_path, monkeypatch):
        """A file literally named 'hook' must not shadow the subcommand."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "hook").write_text("not markdown")
        monkeypatch.setenv("HOME", str(tmp_path))
        monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
        monkeypatch.delenv("MARKDOWN_FIXER_HOOK", raising=False)

        # Unarmed, so the hook is a no-op that exits 0 without reading stdin.
        code = run_cli(["hook", "claude-code"])
        assert code == 0

    def test_hook_requires_a_known_host(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        code = run_cli(["hook", "not-a-real-host"])
        assert code == 2

    def test_bare_file_mode_still_works(self, tmp_path, capsys):
        test_file = tmp_path / "test.md"
        test_file.write_text("# Header\n- List item\nText")
        code = run_cli([str(test_file), "--in-place"])
        assert code == 0
        assert "Formatted" in capsys.readouterr().out

    def test_reserved_set_contents(self):
        from markdown_fixer.cli import RESERVED

        assert RESERVED == frozenset({"hook", "mcp-server", "doctor"})
