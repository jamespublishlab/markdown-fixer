#!/usr/bin/env python3
"""
Machine-local configuration for markdown-fixer.

Config lives at $XDG_CONFIG_HOME/markdown-fixer/config.json, falling back to
~/.config/markdown-fixer/config.json.

    {
      "hook_enabled": true,
      "exclude_patterns": ["(^|/)(Daily|Weekly)/"],
      "strip_horizontal_rules": false
    }

The config file — not settings.json — is the durable arming signal, so the
Claude Code hook line can stay byte-identical on every machine.

strip_horizontal_rules defaults to False here, the opposite of the library and
CLI default. The hook and MCP server rewrite documents the user handed to
another tool, not to the formatter, so removing a `---` is a structural edit
they did not ask for -- and it silently breaks any format using rules as
section separators. Explicit CLI invocation is different: there the
reformatting is the request.

Write patterns to match every path shape the hook can see: Write supplies
an absolute path, but the Obsidian MCP tools supply a path relative to the
vault root instead (e.g. "Daily/x.md", not "/Users/you/.../Daily/x.md"). A
pattern anchored with "^~/..." matches only the absolute form. is_excluded()
matches unanchored (re.search), so an anchor-free pattern like the one above
matches both.

The config fails closed. An unparseable file, an exclude_patterns that is not
a JSON array, and a non-string *entry* inside that array all mark the config
malformed, which forces the hook unarmed even against a truthy env var: a
config whose exclusion set cannot be read in full is a config whose intent is
unknown, and running the fixer with silently fewer exclusions than were asked
for is the data-loss direction.

PATTERNS_ENV_VAR is the deliberate exception. It only ADDS patterns, so a bad
value there cannot shrink what the config already protects -- a bad entry is
warned about and skipped, never disarming.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from typing import Pattern as RePattern

HOOK_ENV_VAR = "MARKDOWN_FIXER_HOOK"
PATTERNS_ENV_VAR = "MARKDOWN_FIXER_EXCLUDE_PATTERNS"
# Not ours, but it decides which config file exists at all, so it belongs in
# any report about where the config came from.
CONFIG_HOME_ENV_VAR = "XDG_CONFIG_HOME"

TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
FALSE_VALUES = frozenset({"0", "false", "no", "off"})


@dataclass
class Pattern:
    """One exclusion pattern, with where it came from and whether it compiled."""

    raw: str
    source: str  # "config" or "env"
    regex: Optional[RePattern] = None
    error: Optional[str] = None

    @property
    def valid(self):
        return self.regex is not None


@dataclass
class Config:
    """Parsed config state. `malformed` means the file existed but was unusable."""

    path: Optional[Path] = None
    hook_enabled: bool = False
    raw_patterns: List[str] = field(default_factory=list)
    strip_horizontal_rules: bool = False
    malformed: bool = False


def config_path():
    """Return the config file path. The file may not exist."""
    xdg = os.environ.get(CONFIG_HOME_ENV_VAR)
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "markdown-fixer" / "config.json"


def collapse_home(path):
    """Rewrite a leading home directory to '~'.

    Returns the path unchanged when it does not start with the home directory,
    so callers can match against both forms unconditionally.
    """
    home = str(Path.home())
    if path == home:
        return "~"
    if path.startswith(home + os.sep):
        return "~" + path[len(home) :]
    return path


def load_config():
    """Read and parse the config file. Never raises."""
    path = config_path()

    # Read without an exists() pre-check. exists() swallows only ENOENT,
    # ENOTDIR, EBADF and ELOOP, so EACCES escaped it -- and only on Python
    # <= 3.12, since 3.13 broadened it to catch every OSError. That made the
    # escape invisible on a modern interpreter while it still reached
    # /usr/bin/python3 3.9.6, which this project ships against. Opening the
    # file raises the same way everywhere, so the missing case is separated by
    # exception type instead: absent is the normal state under opt-in arming
    # and must stay distinct from unreadable, which fails closed.
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return Config()
    except (OSError, ValueError) as exc:
        print(f"markdown-fixer: cannot read config {path}: {exc}", file=sys.stderr)
        return Config(path=path, malformed=True)

    if not isinstance(data, dict):
        print(f"markdown-fixer: config {path} is not a JSON object", file=sys.stderr)
        return Config(path=path, malformed=True)

    exclude_patterns = data.get("exclude_patterns", [])
    if not isinstance(exclude_patterns, list):
        print(
            f"markdown-fixer: config {path}: exclude_patterns must be a JSON array",
            file=sys.stderr,
        )
        return Config(path=path, malformed=True)

    for index, pattern in enumerate(exclude_patterns):
        if not isinstance(pattern, str):
            # Fail closed like a non-array exclude_patterns does: dropping the
            # entry would leave the hook armed with fewer exclusions than the
            # config asks for. Name the index so the entry can be found.
            print(
                f"markdown-fixer: config {path}: exclude_patterns[{index}] is "
                f"{type(pattern).__name__}, not a string",
                file=sys.stderr,
            )
            return Config(path=path, malformed=True)

    # Absent means False: not stripping is the safe direction, and a bad value
    # here cannot shrink protection the way a bad exclude_patterns entry can,
    # so it warns and falls back rather than marking the config malformed.
    strip_rules = data.get("strip_horizontal_rules", False)
    if not isinstance(strip_rules, bool):
        print(
            f"markdown-fixer: config {path}: strip_horizontal_rules must be true or "
            f"false, got {type(strip_rules).__name__}; treating it as false",
            file=sys.stderr,
        )
        strip_rules = False

    return Config(
        path=path,
        hook_enabled=data.get("hook_enabled") is True,
        raw_patterns=list(exclude_patterns),
        strip_horizontal_rules=strip_rules,
    )


def _env_flag(name):
    """True/False for an explicitly recognised value, None otherwise.

    None covers unset, empty, and typos. A typo must not force the hook off --
    it simply fails to arm, deferring to the config file.
    """
    raw = os.environ.get(name)
    if raw is None:
        return None
    value = raw.strip().lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    return None


def is_armed(cfg):
    """Decide whether the hook should run.

    A malformed config forces unarmed even against a truthy env var: an
    unreadable config means the exclusion set is unknown, and running with
    silently-empty exclusions is the data-risk direction.
    """
    if cfg.malformed:
        return False

    flag = _env_flag(HOOK_ENV_VAR)
    if flag is False:
        return False
    if flag is True:
        return True
    return cfg.hook_enabled


def _env_patterns():
    """Parse PATTERNS_ENV_VAR as a JSON array of strings. Never raises."""
    raw = os.environ.get(PATTERNS_ENV_VAR)
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except ValueError as exc:
        print(f"markdown-fixer: {PATTERNS_ENV_VAR} is not valid JSON: {exc}", file=sys.stderr)
        return []

    if not isinstance(data, list):
        print(f"markdown-fixer: {PATTERNS_ENV_VAR} must be a JSON array", file=sys.stderr)
        return []

    # Unlike the config file, a bad entry here warns and is skipped rather than
    # disarming: env patterns only ADD to the config's, so one cannot shrink
    # the protection the config already provides. Disarming over a single bad
    # entry would also punish it harder than a wholly unparseable value, which
    # is already only warned about.
    patterns = []
    for index, pattern in enumerate(data):
        if not isinstance(pattern, str):
            print(
                f"markdown-fixer: {PATTERNS_ENV_VAR}[{index}] is "
                f"{type(pattern).__name__}, not a string; ignoring it",
                file=sys.stderr,
            )
            continue
        patterns.append(pattern)
    return patterns


def _compile_one(raw, source):
    try:
        return Pattern(raw=raw, source=source, regex=re.compile(raw))
    except re.error as exc:
        print(
            f"markdown-fixer: ignoring invalid exclude pattern {raw!r}: {exc}",
            file=sys.stderr,
        )
        return Pattern(raw=raw, source=source, error=str(exc))


def compile_patterns(cfg):
    """Compile config patterns then env patterns. Env patterns ADD to config."""
    patterns = [_compile_one(raw, "config") for raw in cfg.raw_patterns]
    patterns.extend(_compile_one(raw, "env") for raw in _env_patterns())
    return patterns


def is_excluded(filepath, patterns):
    """True when filepath matches any valid pattern.

    Every pattern is tested against both the raw path and its home-collapsed
    form, so a config written either way works on any machine. When the path is
    not under home the two forms are identical and the pattern is simply tested
    twice.

    Neither form helps a caller that never sends an absolute path in the
    first place: the Obsidian MCP tools pass filenames relative to the vault
    root (e.g. "Daily/x.md"), so a home-anchored pattern like "^~/.../Daily/"
    cannot match what they send, regardless of this function's own logic.
    There is no vault root to resolve against here -- the fix is an
    unanchored pattern (see module docstring), not a change to this
    function.
    """
    candidates = {filepath, collapse_home(filepath)}
    for pattern in patterns:
        if not pattern.valid:
            continue
        for candidate in candidates:
            if pattern.regex.search(candidate):
                return True
    return False
