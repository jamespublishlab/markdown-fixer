"""MCP speaks JSON-RPC over stdout, so nothing else may be written there.

A stray print, a traceback, or an unguarded exception escaping the stdin read
loop would corrupt the protocol stream in a way that is very hard to diagnose
from inside Claude Desktop.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Syntactically valid JSON, but not a JSON-RPC request object. A buggy or
# malicious client can send this; the server must not let it crash the read
# loop and take the rest of the session down with it.
NOT_AN_OBJECT = json.dumps(123)

INITIALIZE = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})


def test_stdout_contains_only_jsonrpc_frames(tmp_path):
    """A non-object frame followed by a real request must not corrupt or halt
    stdout: every line the server writes must be a valid JSON-RPC 2.0 frame,
    and the server must still answer the request that follows."""
    env = dict(os.environ)
    env["HOME"] = str(tmp_path)  # isolate from the developer's real config
    env["PYTHONPATH"] = str(REPO_ROOT / "src")

    result = subprocess.run(
        [sys.executable, "-m", "markdown_fixer.mcp_server"],
        input=NOT_AN_OBJECT + "\n" + INITIALIZE + "\n",
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert lines, f"no protocol output; stderr was: {result.stderr}"

    for line in lines:
        frame = json.loads(line)  # raises if anything non-JSON reached stdout
        assert frame["jsonrpc"] == "2.0"

    # The malformed frame must not have knocked the loop over: the server
    # must still have processed and answered the initialize request.
    assert len(lines) == 2, f"expected 2 frames (error + initialize), got: {lines}"
