"""Tests for the Claude Code PreToolUse hook.

This surface had zero coverage before -- it lived outside the package, which is
precisely why a silent-data-loss bug survived in this project for its whole
lifetime.
"""

import io
import json

import pytest

from markdown_fixer import config as cfgmod
from markdown_fixer import hook as hookmod

# Content the fixer demonstrably rewrites (a list needing surrounding blanks).
DIRTY = "# Header\n- List item\nText"
# Content the fixer leaves alone.
CLEAN = "# Header\n\nJust a paragraph.\n"


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    monkeypatch.delenv(cfgmod.HOOK_ENV_VAR, raising=False)
    monkeypatch.delenv(cfgmod.PATTERNS_ENV_VAR, raising=False)
    return tmp_path


def write_config(home_dir, data):
    target = home_dir / ".config" / "markdown-fixer"
    target.mkdir(parents=True, exist_ok=True)
    path = target / "config.json"
    path.write_text(data if isinstance(data, str) else json.dumps(data))
    return path


def payload(filename, content=DIRTY, key="file_path"):
    return json.dumps({"tool_input": {key: str(filename), "content": content}})


def run_hook(raw_stdin):
    """Run the hook against a stdin string; return (exit_code, stdout_text)."""
    out = io.StringIO()
    code = hookmod.run(stdin=io.StringIO(raw_stdin), stdout=out)
    return code, out.getvalue()


class TestArming:
    def test_unarmed_produces_no_output(self, home):
        code, out = run_hook(payload(home / "doc.md"))
        assert code == 0
        assert out == ""

    def test_armed_via_config_rewrites(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload(home / "doc.md"))
        assert code == 0
        assert json.loads(out)["hookSpecificOutput"]["hookEventName"] == "PreToolUse"

    def test_armed_via_env(self, home, monkeypatch):
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        code, out = run_hook(payload(home / "doc.md"))
        assert code == 0
        assert out != ""

    def test_env_zero_overrides_config(self, home, monkeypatch):
        write_config(home, {"hook_enabled": True})
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "0")
        code, out = run_hook(payload(home / "doc.md"))
        assert code == 0
        assert out == ""


class TestGates:
    def test_malformed_stdin_exits_zero(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook("{not json")
        assert code == 0
        assert out == ""

    def test_missing_filename_exits_zero(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(json.dumps({"tool_input": {"content": DIRTY}}))
        assert code == 0
        assert out == ""

    def test_non_markdown_file_is_skipped(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload(home / "script.py"))
        assert code == 0
        assert out == ""

    def test_obsidian_filename_key_is_honoured(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload(home / "doc.md", key="filename"))
        assert code == 0
        assert out != ""

    def test_empty_content_is_skipped(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload(home / "doc.md", content=""))
        assert code == 0
        assert out == ""

    def test_unchanged_content_produces_no_output(self, home):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload(home / "doc.md", content=CLEAN))
        assert code == 0
        assert out == ""


class TestExclusions:
    def test_excluded_by_raw_path(self, home):
        write_config(home, {"hook_enabled": True, "exclude_patterns": [f"^{home}/Daily/"]})
        code, out = run_hook(payload(home / "Daily" / "doc.md"))
        assert code == 0
        assert out == ""

    def test_excluded_by_home_collapsed_form(self, home):
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/Daily/"]})
        code, out = run_hook(payload(home / "Daily" / "doc.md"))
        assert code == 0
        assert out == ""

    def test_invalid_pattern_is_ignored_and_hook_still_runs(self, home, capsys):
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/foo["]})
        code, out = run_hook(payload(home / "doc.md"))
        assert code == 0
        assert out != ""
        assert "ignoring invalid exclude pattern" in capsys.readouterr().err


class TestOutputShape:
    def test_updated_input_preserves_other_keys(self, home):
        write_config(home, {"hook_enabled": True})
        raw = json.dumps(
            {"tool_input": {"file_path": str(home / "doc.md"), "content": DIRTY, "extra": 7}}
        )
        code, out = run_hook(raw)
        updated = json.loads(out)["hookSpecificOutput"]["updatedInput"]

        assert code == 0
        assert updated["extra"] == 7
        assert updated["file_path"] == str(home / "doc.md")
        assert updated["content"] != DIRTY

    def test_permission_decision_is_allow(self, home):
        write_config(home, {"hook_enabled": True})
        _, out = run_hook(payload(home / "doc.md"))
        assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "allow"
