"""Tests for machine-local configuration."""

import json

import pytest

from markdown_fixer import config as cfgmod


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

    def test_non_string_patterns_are_dropped(self, home):
        write_config(home, {"exclude_patterns": ["^~/Daily/", 7, None]})
        assert cfgmod.load_config().raw_patterns == ["^~/Daily/"]


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
