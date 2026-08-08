"""
Report markdown-fixer's resolved state.

Answers "is this armed on this machine, and what will it skip?".

It deliberately does NOT claim to answer "can Claude Code find this?". doctor
runs in the user's shell with the user's PATH, while hooks and MCP servers
inherit their parent process's environment instead -- so it is structurally
blind to their PATH. Diagnosing that requires reading the parent process
environment (`ps eww -p <pid>`).
"""

import os
import sys
from pathlib import Path

from .__version__ import __version__
from .config import (
    HOOK_ENV_VAR,
    PATTERNS_ENV_VAR,
    _env_flag,
    compile_patterns,
    config_path,
    is_armed,
    load_config,
)


def _install_form():
    """Return "zipapp" or "package", detected at runtime.

    Inside a zipapp __file__ points within the archive, so the package
    directory is not a real directory on disk.
    """
    package_dir = Path(__file__).resolve().parent
    return "package" if package_dir.is_dir() else "zipapp"


def arming_source(cfg):
    """Describe what armed the hook, or why it did not arm.

    Mirrors config.is_armed()'s own three-way split on HOOK_ENV_VAR, reusing
    its private classifier (config._env_flag) rather than re-deriving
    true/false-ness here -- duplicating that normalisation would risk silently
    drifting out of sync with is_armed() and misreporting what actually arms
    the hook:

    - malformed config: forces unarmed regardless of the env var.
    - a *recognised* env value (a true or false spelling): decisively
      overrides config either way, since is_armed() short-circuits on it.
    - a *set but unrecognised* env value (a typo, or an empty string): does
      NOT force anything -- is_armed() silently ignores it and defers to the
      config file alone. The report must say so explicitly rather than
      implying the env var contributed, or blaming it for being off.
    """
    if cfg.malformed:
        return "NOT ARMED (config unreadable -- fail closed)"

    env_raw = os.environ.get(HOOK_ENV_VAR)
    armed = is_armed(cfg)

    if env_raw is None:
        return f"ARMED via config {cfg.path}" if armed else "NOT ARMED"

    env_flag = _env_flag(HOOK_ENV_VAR)  # True/False if recognised, else None
    if env_flag is None:
        note = f" ({HOOK_ENV_VAR}={env_raw!r} is unrecognised, ignored)"
        return f"ARMED via config {cfg.path}{note}" if armed else f"NOT ARMED{note}"

    # A recognised value decisively determined the outcome (is_armed() only
    # falls through to cfg.hook_enabled when env_flag is None).
    if env_flag:
        return f"ARMED via {HOOK_ENV_VAR}={env_raw!r}"
    return f"NOT ARMED ({HOOK_ENV_VAR}={env_raw!r})"


def report(stdout=None):
    """Print the resolved state. Always returns 0."""
    stdout = stdout if stdout is not None else sys.stdout

    cfg = load_config()
    patterns = compile_patterns(cfg)

    entry_point = Path(sys.argv[0]).resolve() if sys.argv and sys.argv[0] else "?"

    lines = [
        f"executable   {entry_point} ({_install_form()}, {__version__})",
        f"python       {sys.version.split()[0]} ({sys.executable})",
        f"hook         {arming_source(cfg)}",
        f"config       {cfg.path if cfg.path else f'{config_path()} (absent)'}",
    ]

    if not patterns:
        lines.append("patterns     (none)")
    else:
        label = "patterns    "
        for pattern in patterns:
            status = "ok     " if pattern.valid else f"INVALID: {pattern.error}"
            lines.append(f"{label} {pattern.raw}   {status}   [{pattern.source}]")
            label = "            "

    lines.append("")
    lines.append("note         doctor sees THIS shell's PATH. Hooks and MCP servers inherit")
    lines.append(f"             their parent process's environment instead. {HOOK_ENV_VAR},")
    lines.append(f"             {PATTERNS_ENV_VAR}, and PATH may all differ there.")

    stdout.write("\n".join(lines) + "\n")
    return 0
