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
    monkeypatch.delenv(cfgmod.FIXES_ENV_VAR, raising=False)
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

    @pytest.mark.parametrize("bad_value", [123, ["a.md"], {"p": "a.md"}, True])
    def test_non_string_filename_exits_zero(self, home, bad_value):
        """A malformed payload must never raise out of the hook."""
        write_config(home, {"hook_enabled": True})
        raw = json.dumps({"tool_input": {"file_path": bad_value, "content": DIRTY}})
        code, out = run_hook(raw)
        assert code == 0
        assert out == ""

    def test_recursion_error_from_json_load_exits_zero(self, home, monkeypatch):
        """run()'s docstring promises "Always returns 0". json.load() raises
        RecursionError -- not ValueError or OSError -- on deeply nested input,
        so a narrow except clause would let it escape uncaught.

        Forced rather than provoked: raising directly tests the contract on
        every interpreter, instantly, instead of depending on whatever the
        current recursion limit happens to be."""
        write_config(home, {"hook_enabled": True})

        def boom(*_a, **_kw):
            raise RecursionError("maximum recursion depth exceeded")

        monkeypatch.setattr(hookmod.json, "load", boom)
        code, out = run_hook(payload("/tmp/x.md"))
        assert code == 0
        assert out == ""

    def test_pathologically_deep_json_exits_zero(self, home):
        """The realistic counterpart to the forced test above.

        The precondition matters: `[[[...]]]` that PARSES yields a list, which
        the hook rejects at the isinstance(dict) check and returns 0 for with
        no output -- identical to the RecursionError outcome. Without asserting
        that json actually raises, this test would pass whether or not the path
        under test is reached at all."""
        write_config(home, {"hook_enabled": True})
        depth = 200_000
        deeply_nested = "[" * depth + "]" * depth

        try:
            json.loads(deeply_nested)
        except RecursionError:
            pass
        else:
            pytest.skip("this interpreter parses the input without recursing")

        code, out = run_hook(deeply_nested)
        assert code == 0
        assert out == ""

    def test_broken_pipe_on_write_exits_zero(self, home, monkeypatch):
        """The consumer can close the pipe before the hook writes its output.

        json.dump then raises BrokenPipeError mid-write. run() must still
        return 0: an exception here would surface as a hook failure on a write
        that was otherwise fine."""
        write_config(home, {"hook_enabled": True})

        def boom(*_a, **_kw):
            raise BrokenPipeError(32, "Broken pipe")

        monkeypatch.setattr(hookmod.json, "dump", boom)
        # DIRTY is rewritten by the fixer, so the dump path is genuinely reached
        code, out = run_hook(payload("/tmp/x.md", content=DIRTY))
        assert code == 0
        assert out == ""

    def test_the_broken_pipe_test_reaches_the_dump(self, home):
        """Guard for the test above: if DIRTY ever stopped being rewritten,
        the hook would return early and that test would pass vacuously."""
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload("/tmp/x.md", content=DIRTY))
        assert code == 0
        assert out, "DIRTY no longer triggers a rewrite; the BrokenPipe test is now vacuous"


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

    def test_excluded_by_vault_relative_filename(self, home):
        """Obsidian MCP tools pass a VAULT-RELATIVE filename (e.g. 'Daily/x.md'),
        not an absolute path, so a pattern anchored at ^~/... can never match it.
        A pattern written to match both forms -- the recommended style -- must
        work for both the vault-relative caller (Obsidian MCP) AND the
        absolute-path caller (Write/Edit)."""
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["(^|/)(Daily|Weekly)/"]})

        code, out = run_hook(payload("Daily/2026-08-08.md", key="filename"))
        assert code == 0
        assert out == ""

        code, out = run_hook(payload(home / "Weekly" / "2026-W32.md"))
        assert code == 0
        assert out == ""

    def test_home_anchored_pattern_misses_vault_relative_filename(self, home):
        """Documents the trap: an absolute-anchored pattern does NOT protect
        Obsidian MCP writes. If this ever starts passing, the matching semantics
        changed and the docs need revisiting."""
        write_config(
            home,
            {
                "hook_enabled": True,
                "exclude_patterns": ["^~/Documents/SecondBrain/Daily/"],
            },
        )
        code, out = run_hook(payload("Daily/2026-08-08.md", key="filename"))
        assert code == 0
        assert out != ""  # NOT protected -- the pattern cannot match


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


class TestHorizontalRuleGating:
    """The hook must not strip `---` unless the machine config opts in.

    This is why `_wip/` had to be excluded before: the WIP format uses `---`
    both as a section separator and as an edit anchor, so unconditional
    removal silently broke it.
    """

    RULED = "Section one\n\n---\n\n- a\n- b\nTrailing text"

    def test_default_config_preserves_rules(self, home, tmp_path):
        write_config(home, {"hook_enabled": True})
        code, out = run_hook(payload(tmp_path / "note.md", content=self.RULED))
        assert code == 0
        assert out, "hook should still fire (the list spacing needs fixing)"
        cleaned = json.loads(out)["hookSpecificOutput"]["updatedInput"]["content"]
        assert "\n---\n" in cleaned, "rule was stripped despite the safe default"
        assert "- a" in cleaned and "Trailing text" in cleaned

    def test_opt_in_true_strips_rules(self, home, tmp_path):
        write_config(home, {"hook_enabled": True, "strip_horizontal_rules": True})
        code, out = run_hook(payload(tmp_path / "note.md", content=self.RULED))
        assert code == 0
        cleaned = json.loads(out)["hookSpecificOutput"]["updatedInput"]["content"]
        assert "\n---\n" not in cleaned, "opt-in did not re-enable stripping"

    def test_rule_only_change_is_now_a_no_op(self, home, tmp_path):
        """A file whose ONLY 'problem' was a rule must pass through untouched."""
        write_config(home, {"hook_enabled": True})
        src = "Above the rule.\n\n---\n\nBelow the rule.\n"
        code, out = run_hook(payload(tmp_path / "note.md", content=src))
        assert code == 0
        assert out == "", "hook rewrote a file it no longer needs to change"
