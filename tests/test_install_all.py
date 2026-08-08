"""Tests for scripts/install-all.sh's CLI (zipapp) install path.

The `rm -f` before `cp` in the install block is load-bearing, not hygiene:
~/.local/bin/markdown-fixer may already be a symlink into an old pipx venv,
and `cp` follows symlinks -- without the `rm -f` it would overwrite the
venv's own binary in place, leaving the symlink pointing at the new zipapp
while the venv silently rots underneath it. That semi-works, which is worse
than failing outright: it survives casual testing and breaks confusingly
later.

A plain throwaway-HOME run can't catch a regression here, because a fresh
HOME has no pre-existing symlink at the target path -- `rm -f` on a
nonexistent file and no `rm -f` at all look identical. This test manufactures
the symlink first, so the assertion actually discriminates.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SCRIPT = REPO_ROOT / "scripts" / "install-all.sh"

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="the zipapp install path is POSIX-only; Windows uses pip install",
)


def run_installer(home, extra_path_dirs=()):
    """Run `install-all.sh --cli` against a throwaway HOME.

    Unlike test_zipapp.py's minimal env dict, TERM must survive: the script
    calls `clear` near the top under `set -e`, and a stripped TERM makes
    `clear` fail there, aborting the script before the CLI block ever runs.
    Starting from a copy of os.environ keeps TERM (and other ambient
    settings) intact while HOME and PATH are pinned explicitly.
    """
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["PYTHONNOUSERSITE"] = "1"
    env["PATH"] = ":".join([*extra_path_dirs, "/usr/bin", "/bin", "/usr/local/bin"])
    return subprocess.run(
        ["bash", str(INSTALL_SCRIPT), "--cli"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )


def run_artifact(path, args):
    """Run an installed binary with no user site-packages, mirroring
    test_zipapp.py's run_artifact."""
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ["HOME"], "PYTHONNOUSERSITE": "1"}
    return subprocess.run(
        [str(path)] + list(args),
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def test_overwrites_pipx_symlink_and_installs_both_binaries(tmp_path):
    bin_dir = tmp_path / ".local" / "bin"
    bin_dir.mkdir(parents=True)
    fake_venv_bin = tmp_path / "fake-venv-bin"
    fake_venv_bin.write_text("SENTINEL\n")
    target = bin_dir / "markdown-fixer"
    target.symlink_to(fake_venv_bin)

    result = run_installer(tmp_path)

    assert result.returncode == 0, result.stderr

    # The old "venv" binary must be untouched. If cp had followed the
    # symlink instead of rm -f removing it first, this file would now
    # contain the zipapp's bytes instead of the sentinel.
    assert fake_venv_bin.read_text() == "SENTINEL\n"

    assert target.exists()
    assert not target.is_symlink(), "markdown-fixer must be a regular file, not a symlink"

    alias = bin_dir / "mdfixer"
    assert alias.is_symlink()
    assert alias.resolve() == target.resolve()

    # A throwaway bin_dir is never on PATH, so the loud warning must fire --
    # this is the failure mode the whole project exists to eliminate.
    assert "is NOT on your PATH" in result.stdout

    for name in ("markdown-fixer", "mdfixer"):
        version = run_artifact(bin_dir / name, ["--version"])
        assert version.returncode == 0, version.stderr
        assert "markdown-fixer, version" in version.stdout


def test_no_path_warning_when_bin_dir_already_on_path(tmp_path):
    bin_dir = tmp_path / ".local" / "bin"
    bin_dir.mkdir(parents=True)

    result = run_installer(tmp_path, extra_path_dirs=(str(bin_dir),))

    assert result.returncode == 0, result.stderr
    assert "is NOT on your PATH" not in result.stdout
    assert "is on PATH" in result.stdout
