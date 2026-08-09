"""Tests for machine-local configuration."""

import json
import os
import sys

import pytest

from markdown_fixer import config as cfgmod

# chmod does not gate reads for root, and does not gate them at all on Windows.
needs_enforced_permissions = pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="directory permissions are not enforced for root or on Windows",
)


@pytest.fixture
def home(tmp_path, monkeypatch):
    """Isolate HOME and clear both env vars for every test."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    monkeypatch.delenv(cfgmod.HOOK_ENV_VAR, raising=False)
    monkeypatch.delenv(cfgmod.PATTERNS_ENV_VAR, raising=False)
    return tmp_path


def write_config(home_dir, data, xdg=None):
    """Write a config file and return its path."""
    base = xdg if xdg else home_dir / ".config"
    target = base / "markdown-fixer"
    target.mkdir(parents=True, exist_ok=True)
    path = target / "config.json"
    path.write_text(data if isinstance(data, str) else json.dumps(data))
    return path


class TestConfigPath:
    def test_prefers_xdg_config_home(self, home, monkeypatch, tmp_path):
        xdg = tmp_path / "xdg"
        monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))
        assert cfgmod.config_path() == xdg / "markdown-fixer" / "config.json"

    def test_falls_back_to_dot_config(self, home):
        assert cfgmod.config_path() == home / ".config" / "markdown-fixer" / "config.json"


class TestLoadConfig:
    def test_missing_file_is_not_an_error(self, home):
        cfg = cfgmod.load_config()
        assert cfg.path is None
        assert cfg.hook_enabled is False
        assert cfg.raw_patterns == []
        assert cfg.malformed is False

    def test_malformed_json_is_flagged(self, home, capsys):
        write_config(home, "{not json")
        cfg = cfgmod.load_config()
        assert cfg.malformed is True
        assert "cannot read config" in capsys.readouterr().err

    def test_non_object_json_is_malformed(self, home, capsys):
        write_config(home, "[1, 2, 3]")
        cfg = cfgmod.load_config()
        assert cfg.malformed is True
        assert "not a JSON object" in capsys.readouterr().err

    def test_valid_config_is_read(self, home):
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/Daily/"]})
        cfg = cfgmod.load_config()
        assert cfg.hook_enabled is True
        assert cfg.raw_patterns == ["^~/Daily/"]
        assert cfg.malformed is False

    def test_unknown_keys_are_ignored(self, home):
        write_config(home, {"hook_enabled": True, "nonsense": 42})
        assert cfgmod.load_config().hook_enabled is True

    @pytest.mark.parametrize("bad", [7, None, ["(^|/)Daily/"]])
    def test_non_string_pattern_entry_is_malformed(self, home, capsys, bad):
        """A non-string *entry* fails closed, exactly as a non-array
        exclude_patterns does.

        Dropping it silently -- the previous behaviour -- left the hook ARMED
        with fewer exclusions than the config asks for, which is the
        armed-with-unknown-exclusions outcome the fail-closed rule exists to
        prevent. A nested list is the likely typo, and was the reported case.
        The warning names the index so the offending entry is findable.
        """
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/Daily/", bad]})
        cfg = cfgmod.load_config()
        captured = capsys.readouterr()

        assert cfg.malformed is True
        assert cfgmod.is_armed(cfg) is False
        assert "exclude_patterns[1]" in captured.err
        assert captured.out == ""

    def test_null_exclude_patterns_is_malformed(self, home, capsys):
        write_config(home, {"hook_enabled": True, "exclude_patterns": None})
        cfg = cfgmod.load_config()
        assert cfg.malformed is True
        assert "must be a JSON array" in capsys.readouterr().err

    def test_bare_string_exclude_patterns_is_malformed(self, home, capsys):
        """A bare string would otherwise iterate character-by-character, and the
        lone '^' would silently exclude every file."""
        write_config(home, {"hook_enabled": True, "exclude_patterns": "^~/Daily/"})
        cfg = cfgmod.load_config()
        assert cfg.malformed is True
        assert "must be a JSON array" in capsys.readouterr().err

    def test_malformed_exclude_patterns_forces_unarmed(self, home):
        """hook_enabled: true must not survive an unreadable exclusion set."""
        write_config(home, {"hook_enabled": True, "exclude_patterns": 42})
        assert cfgmod.is_armed(cfgmod.load_config()) is False

    @needs_enforced_permissions
    def test_unreadable_config_dir_is_malformed_and_does_not_raise(self, home, capsys):
        """An EACCES on the config path must fail closed, not escape.

        load_config() is contractually "never raises", and hook.run() calls it
        outside any try. The guard that used to sit above the try was
        `path.exists()`, which only swallows ENOENT/ENOTDIR/EBADF/ELOOP -- so
        EACCES propagated, and did so only on Python <= 3.12 (3.13 broadened
        exists() to catch every OSError). That made the escape invisible on a
        modern dev interpreter while it still bit /usr/bin/python3 3.9.6, the
        floor this project ships against. Reading the file directly raises on
        every version, so this assertion is version-independent.
        """
        path = write_config(home, {"hook_enabled": True})
        path.parent.chmod(0o000)
        try:
            cfg = cfgmod.load_config()
        finally:
            path.parent.chmod(0o755)
        captured = capsys.readouterr()

        assert cfg.malformed is True
        assert cfgmod.is_armed(cfg) is False
        assert "cannot read config" in captured.err
        assert captured.out == ""

    def test_warnings_never_reach_stdout(self, home, capsys):
        """A later task speaks JSON-RPC over stdout; a stray print would corrupt it."""
        write_config(home, "{not json")
        cfgmod.compile_patterns(cfgmod.load_config())
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err != ""


class TestIsArmed:
    def test_config_arms(self, home):
        write_config(home, {"hook_enabled": True})
        assert cfgmod.is_armed(cfgmod.load_config()) is True

    def test_env_arms_without_config(self, home, monkeypatch):
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        assert cfgmod.is_armed(cfgmod.load_config()) is True

    def test_env_falsy_overrides_config(self, home, monkeypatch):
        write_config(home, {"hook_enabled": True})
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "0")
        assert cfgmod.is_armed(cfgmod.load_config()) is False

    def test_malformed_config_beats_truthy_env(self, home, monkeypatch):
        """Fail closed: unknown exclusions plus a running fixer is the
        data-risk direction."""
        write_config(home, "{not json")
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        assert cfgmod.is_armed(cfgmod.load_config()) is False

    def test_typo_defers_to_config(self, home, monkeypatch):
        """A typo neither arms nor forces off."""
        write_config(home, {"hook_enabled": True})
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "ture")
        assert cfgmod.is_armed(cfgmod.load_config()) is True

    def test_nothing_set_is_unarmed(self, home):
        assert cfgmod.is_armed(cfgmod.load_config()) is False

    def test_explicit_false_config_with_truthy_env_arms(self, home, monkeypatch):
        write_config(home, {"hook_enabled": False})
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        assert cfgmod.is_armed(cfgmod.load_config()) is True

    def test_explicit_false_config_without_env_is_unarmed(self, home):
        write_config(home, {"hook_enabled": False})
        assert cfgmod.is_armed(cfgmod.load_config()) is False


class TestCollapseHome:
    def test_collapses_home_prefix(self, home):
        assert cfgmod.collapse_home(str(home / "Documents" / "x.md")) == "~/Documents/x.md"

    def test_leaves_other_paths_alone(self, home):
        assert cfgmod.collapse_home("/etc/hosts") == "/etc/hosts"


class TestExclusion:
    def test_matches_raw_absolute_path(self, home):
        write_config(home, {"exclude_patterns": [f"^{home}/Daily/"]})
        patterns = cfgmod.compile_patterns(cfgmod.load_config())
        assert cfgmod.is_excluded(str(home / "Daily" / "note.md"), patterns) is True

    def test_matches_home_collapsed_form(self, home):
        write_config(home, {"exclude_patterns": ["^~/Daily/"]})
        patterns = cfgmod.compile_patterns(cfgmod.load_config())
        assert cfgmod.is_excluded(str(home / "Daily" / "note.md"), patterns) is True

    def test_non_matching_path_is_not_excluded(self, home):
        write_config(home, {"exclude_patterns": ["^~/Daily/"]})
        patterns = cfgmod.compile_patterns(cfgmod.load_config())
        assert cfgmod.is_excluded(str(home / "Code" / "note.md"), patterns) is False

    def test_env_patterns_add_to_config_patterns(self, home, monkeypatch):
        write_config(home, {"exclude_patterns": ["^~/Daily/"]})
        monkeypatch.setenv(cfgmod.PATTERNS_ENV_VAR, json.dumps(["/vendor/"]))
        patterns = cfgmod.compile_patterns(cfgmod.load_config())

        assert [p.source for p in patterns] == ["config", "env"]
        assert cfgmod.is_excluded(str(home / "Daily" / "n.md"), patterns) is True
        assert cfgmod.is_excluded("/srv/app/vendor/x.md", patterns) is True

    def test_invalid_regex_is_warned_and_skipped(self, home, capsys):
        write_config(home, {"exclude_patterns": ["^~/foo[", "^~/Daily/"]})
        patterns = cfgmod.compile_patterns(cfgmod.load_config())
        err = capsys.readouterr().err

        assert "ignoring invalid exclude pattern" in err
        assert [p.valid for p in patterns] == [False, True]
        # The valid pattern still works.
        assert cfgmod.is_excluded(str(home / "Daily" / "n.md"), patterns) is True

    def test_malformed_env_var_is_warned_and_ignored(self, home, monkeypatch, capsys):
        monkeypatch.setenv(cfgmod.PATTERNS_ENV_VAR, "{not json")
        patterns = cfgmod.compile_patterns(cfgmod.load_config())

        assert patterns == []
        assert "not valid JSON" in capsys.readouterr().err

    def test_non_string_env_pattern_entry_is_warned_and_skipped(self, home, monkeypatch, capsys):
        """The env var ADDS to config, and a wholly unparseable one is already
        warned-and-ignored without disarming (see the test above). Disarming
        over one bad *entry* would therefore punish a smaller mistake harder
        than a bigger one. Warn, skip the entry, keep the rest -- and the
        config's own patterns must survive untouched."""
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/Daily/"]})
        monkeypatch.setenv(cfgmod.PATTERNS_ENV_VAR, json.dumps(["/vendor/", 7]))
        cfg = cfgmod.load_config()
        patterns = cfgmod.compile_patterns(cfg)
        captured = capsys.readouterr()

        assert cfgmod.is_armed(cfg) is True
        assert [p.raw for p in patterns] == ["^~/Daily/", "/vendor/"]
        assert f"{cfgmod.PATTERNS_ENV_VAR}[1]" in captured.err
        assert captured.out == ""


class TestStripHorizontalRules:
    """`strip_horizontal_rules` gates rule removal on the automatic paths.

    Absent means False -- the safe direction. Removing a rule is a structural
    edit to a document the user did not hand over for reformatting, and the
    `_wip/` exclusion existed solely to work around it being unconditional.
    """

    def test_absent_defaults_to_false(self, home):
        write_config(home, {"hook_enabled": True})
        assert cfgmod.load_config().strip_horizontal_rules is False

    def test_true_is_honoured(self, home):
        write_config(home, {"hook_enabled": True, "strip_horizontal_rules": True})
        assert cfgmod.load_config().strip_horizontal_rules is True

    def test_false_is_honoured(self, home):
        write_config(home, {"hook_enabled": True, "strip_horizontal_rules": False})
        assert cfgmod.load_config().strip_horizontal_rules is False

    def test_no_config_file_defaults_to_false(self, home):
        assert cfgmod.load_config().strip_horizontal_rules is False

    def test_non_bool_warns_and_falls_back_to_false(self, home, capsys):
        write_config(home, {"hook_enabled": True, "strip_horizontal_rules": "yes"})
        cfg = cfgmod.load_config()
        assert cfg.strip_horizontal_rules is False
        assert "strip_horizontal_rules" in capsys.readouterr().err

    def test_non_bool_does_not_mark_the_config_malformed(self, home):
        """Unlike exclude_patterns, a bad value here cannot shrink protection.

        It falls back to the safe direction, so disarming the hook over it
        would punish a typo harder than a wholly unparseable value is.
        """
        write_config(home, {"hook_enabled": True, "strip_horizontal_rules": 1})
        cfg = cfgmod.load_config()
        assert cfg.malformed is False
        assert cfgmod.is_armed(cfg) is True
