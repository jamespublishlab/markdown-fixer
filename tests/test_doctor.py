"""Tests for the doctor subcommand."""

import io
import json

import pytest

from markdown_fixer import config as cfgmod
from markdown_fixer import doctor as docmod


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    monkeypatch.delenv(cfgmod.HOOK_ENV_VAR, raising=False)
    monkeypatch.delenv(cfgmod.PATTERNS_ENV_VAR, raising=False)
    return tmp_path


def write_config(home_dir, data):
    """Write a config file. `data` is JSON-encoded unless already a str, so
    tests can write deliberately malformed JSON (matching test_config.py's
    write_config, which this mirrors -- the brief's version only accepted
    dicts and cannot express a malformed-config case at all)."""
    target = home_dir / ".config" / "markdown-fixer"
    target.mkdir(parents=True, exist_ok=True)
    (target / "config.json").write_text(data if isinstance(data, str) else json.dumps(data))


def report_text():
    out = io.StringIO()
    code = docmod.report(stdout=out)
    return code, out.getvalue()


class TestDoctor:
    def test_reports_unarmed_when_nothing_set(self, home):
        code, text = report_text()
        assert code == 0
        assert "NOT ARMED" in text

    def test_reports_armed_via_config(self, home):
        write_config(home, {"hook_enabled": True})
        _, text = report_text()
        # "ARMED" alone is also a substring of "NOT ARMED" -- assert the
        # unambiguous phrase, and that the negative form is absent, so a
        # report() that is stuck on NOT ARMED cannot pass this test. Bare
        # "config" is even weaker than that: the report's `config <path>`
        # line prints unconditionally in EVERY report regardless of arming
        # state, so it would pass even if arming_source() falsely credited
        # config for an env-driven (or malformed, or unarmed) outcome. Assert
        # the actual attribution phrase arming_source() emits instead.
        assert "ARMED via config" in text
        assert "NOT ARMED" not in text

    def test_reports_armed_via_env(self, home, monkeypatch):
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        _, text = report_text()
        assert "ARMED via" in text
        assert "NOT ARMED" not in text
        # Bare `cfgmod.HOOK_ENV_VAR in text` would no longer discriminate:
        # the PATH-blindness note at the bottom of every report now also
        # names HOOK_ENV_VAR unconditionally (see doctor.py's note block), so
        # that check would pass even if arming_source() never mentioned it.
        # Anchor on the exact attribution phrase arming_source() emits.
        assert f"ARMED via {cfgmod.HOOK_ENV_VAR}=" in text

    def test_labels_pattern_sources(self, home, monkeypatch):
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/Daily/"]})
        monkeypatch.setenv(cfgmod.PATTERNS_ENV_VAR, json.dumps(["/vendor/"]))
        _, text = report_text()
        assert "[config]" in text
        assert "[env]" in text

    def test_flags_invalid_patterns(self, home):
        write_config(home, {"hook_enabled": True, "exclude_patterns": ["^~/foo["]})
        _, text = report_text()
        assert "INVALID" in text

    def test_reports_no_patterns_when_none(self, home, monkeypatch):
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        _, text = report_text()
        assert "(none)" in text

    def test_note_names_the_config_home_variable(self, home):
        """XDG_CONFIG_HOME decides which config file exists at all, so a hook
        whose environment differs there reads a *different config* than the one
        doctor just reported on -- the sharpest form of the drift this note
        exists to warn about, and the one it omitted.

        Assert inside the note block rather than against the whole report:
        doctor prints the resolved `config <path>` line unconditionally, so a
        bare `"XDG_CONFIG_HOME" in text` would be satisfiable by a path that
        merely happens to contain the string.
        """
        _, text = report_text()
        note = text.split("\nnote ", 1)[1]
        assert cfgmod.CONFIG_HOME_ENV_VAR in note

    def test_non_string_pattern_entry_is_not_armed(self, home):
        """A nested list inside exclude_patterns must read as unusable here,
        not as an armed hook with zero exclusions."""
        write_config(home, {"hook_enabled": True, "exclude_patterns": [["(^|/)Daily/"]]})
        code, text = report_text()

        assert code == 0
        assert "NOT ARMED" in text
        assert "ARMED via" not in text


class TestMalformedConfig:
    """report() must never raise, and must fail closed, on an unreadable
    config -- this is a hard global constraint on the task, and the brief's
    own six tests never exercise arming_source()'s cfg.malformed branch."""

    def test_malformed_config_is_not_armed(self, home):
        write_config(home, "{not json")
        code, text = report_text()
        assert code == 0
        assert "NOT ARMED" in text
        assert "unusable" in text

    def test_malformed_config_beats_truthy_env(self, home, monkeypatch):
        """A malformed config forces unarmed even against MARKDOWN_FIXER_HOOK=1 --
        the same fail-closed semantic config.is_armed() enforces."""
        write_config(home, "{not json")
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "1")
        code, text = report_text()
        assert code == 0
        assert "NOT ARMED" in text
        assert "ARMED via" not in text

    def test_malformed_config_warning_stays_on_stderr(self, home, capsys):
        """report()'s output goes only to the caller-provided stream; the
        config-load warning that load_config() prints must land on the
        process's real stderr, never mixed into the injected stdout."""
        write_config(home, "{not json")
        out = io.StringIO()

        code = docmod.report(stdout=out)
        captured = capsys.readouterr()

        assert code == 0
        assert captured.out == ""
        assert "cannot read config" in captured.err
        assert "NOT ARMED" in out.getvalue()


class TestArmingSourceEnvClassification:
    """A set-but-unrecognised HOOK_ENV_VAR (a typo, or an empty string) must
    never be reported as having contributed to the outcome -- config.is_armed()
    silently ignores it and defers to the config file alone. Getting this
    wrong is exactly the kind of misdiagnosis doctor exists to prevent."""

    @pytest.mark.parametrize(
        "env_value,recognised,armed",
        [
            ("1", True, True),
            ("0", True, False),  # recognised falsy overrides hook_enabled: true
            ("TRUE", True, True),
            (" yes ", True, True),
            ("ture", False, True),  # typo -- defers to config, which is armed
            ("", False, True),  # empty string -- same as a typo, defers to config
        ],
    )
    def test_recognition_matches_config_env_flag(
        self, home, monkeypatch, env_value, recognised, armed
    ):
        """Assert the actual armed/unarmed outcome, not just the presence of
        the word "unrecognised" -- a label-only assertion would pass
        identically whether "0" correctly forces the hook off or is (wrongly)
        ignored, leaving the "explicit falsy values force off" semantic from
        the task's arming rules with no assertion that can fail on it."""
        write_config(home, {"hook_enabled": True})
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, env_value)
        _, text = report_text()

        if armed:
            assert "ARMED via" in text
            assert "NOT ARMED" not in text
        else:
            assert f"NOT ARMED ({cfgmod.HOOK_ENV_VAR}=" in text

        if recognised:
            assert "unrecognised" not in text
        else:
            assert "unrecognised" in text
            # A typo must not be credited with arming it -- config alone did.
            assert "ARMED via config" in text
            assert f"ARMED via {cfgmod.HOOK_ENV_VAR}" not in text

    def test_typo_when_config_is_unarmed_is_not_blamed_for_forcing_it_off(self, home, monkeypatch):
        """No config file (hook_enabled defaults False) plus a typo'd env var
        must read as plain NOT ARMED with the typo flagged as ignored -- not
        as if the env var itself forced the hook off (only a recognised
        false value, e.g. "0", can do that)."""
        monkeypatch.setenv(cfgmod.HOOK_ENV_VAR, "ture")
        _, text = report_text()
        assert "NOT ARMED" in text
        assert "unrecognised" in text
