import subprocess
import sys
from pathlib import Path
import pytest

SHELL = Path(__file__).resolve().parents[1] / "app" / "main.py"

def run_shell(commands: str, cwd = None):
    return subprocess.run(
        [sys.executable, str(SHELL)],
        input = commands + "\nexit\n",
        text = True,
        capture_output = True,
        timeout = 5,
        cwd = cwd,
    )

# test echo
@pytest.mark.parametrize(
    "command, expected",
    [
        pytest.param("echo hello123", "hello123", id="single-word"),
        pytest.param("echo hello world", "hello world", id="multiple-word"),
        pytest.param("echo", " ", id="empty"),
        pytest.param("echo hello      world     123", "hello world 123", id="spacey"),
    ],
)

def test_echo(command, expected):
    result = run_shell(command)
    assert expected in result.stdout

# test type
@pytest.mark.parametrize(
    "command, expected",
    [
        pytest.param("type echo", "echo is a shell builtin", id="builtin"),
        pytest.param("type sdfsvfgr", "sdfsvfgr: not found", id="non-existent"),
        pytest.param("type ls", "ls is /usr/bin/ls", id="executable"),
        pytest.param(
            "type grep afdds type vfg",
            ("grep is /usr/bin/grep\n"
            "afdds: not found\n"
            "type is a shell builtin\n"
            "vfg: not found"),
            id="multiple-types"
            ),
    ],
)

def test_type(command, expected):
    result = run_shell(command)
    assert expected in result.stdout

# test exit
def test_exit():
    result = run_shell("exit")
    assert result.returncode == 0