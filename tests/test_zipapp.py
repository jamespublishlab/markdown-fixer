"""Smoke tests that exercise the BUILT zipapp artifact, not the source tree.

The stale-venv incident proved that correct source tells you nothing about what
actually executes. These tests build the artifact and run it as a subprocess.

PYTHONNOUSERSITE=1 is mandatory. This machine has click installed in its user
site-packages, which /usr/bin/python3 adds to sys.path automatically. Without
the flag a zipapp that still imported click would PASS here and fail on any
clean machine.

PATH is pinned to /usr/bin:/bin so the shebang resolves to /usr/bin/python3 --
the same interpreter Claude Desktop uses, which also enforces the 3.8/3.9
syntax floor.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build-zipapp.sh"

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="the zipapp install path is POSIX-only; Windows uses pip install",
)


@pytest.fixture(scope="module")
def zipapp(tmp_path_factory):
    """Build the zipapp once per module and return the artifact path."""
    out_dir = tmp_path_factory.mktemp("zipapp")
    result = subprocess.run(
        ["bash", str(BUILD_SCRIPT), str(out_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"build failed: {result.stderr}"

    artifact = out_dir / "markdown-fixer"
    assert artifact.exists(), "build script did not produce the artifact"
    return artifact


def run_artifact(artifact, args, input=None):
    """Run the built zipapp with no user site-packages and a minimal PATH."""
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": os.environ["HOME"],
        "PYTHONNOUSERSITE": "1",
    }
    return subprocess.run(
        [str(artifact)] + list(args),
        input=input,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


class TestZipappSmoke:
    """The artifact must work with zero third-party dependencies."""

    def test_version_runs(self, zipapp):
        result = run_artifact(zipapp, ["--version"])
        assert result.returncode == 0, result.stderr
        assert "markdown-fixer, version" in result.stdout

    def test_no_missing_module_errors(self, zipapp):
        """Guards the zero-dependency claim explicitly."""
        result = run_artifact(zipapp, ["--version"])
        assert "ModuleNotFoundError" not in result.stderr

    def test_fixes_a_file(self, zipapp, tmp_path):
        target = tmp_path / "doc.md"
        target.write_text("# Header\n- List item\nText")

        result = run_artifact(zipapp, [str(target), "--in-place"])

        assert result.returncode == 0, result.stderr
        assert "\n\n- List item\n\n" in target.read_text()

    def test_exit_code_propagates(self, zipapp, tmp_path):
        """zipapp's generated __main__ does not wrap main() in sys.exit(), so
        main() must call sys.exit() itself or failures report success."""
        result = run_artifact(zipapp, [str(tmp_path / "missing.md")])
        assert result.returncode == 1


class TestZipappMcpServer:
    """The `mcp-server` subcommand must work from the built artifact.

    Before Task 6, mcp_server.py's sys.path hack reached OUTSIDE the package
    for its implementation -- a path that does not exist inside a zip. Making
    this reachable from the zipapp is the entire point of the move.
    """

    def test_mcp_server_answers_initialize(self, zipapp):
        request = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})

        result = run_artifact(zipapp, ["mcp-server"], input=request + "\n")

        assert result.returncode == 0, result.stderr
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        assert lines, f"no protocol output; stderr was: {result.stderr}"

        frame = json.loads(lines[0])  # raises if anything non-JSON reached stdout
        assert frame["jsonrpc"] == "2.0"
        assert frame["id"] == 1
        assert "result" in frame
        assert frame["result"]["serverInfo"]["name"] == "markdown-fixer"
