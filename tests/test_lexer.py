import pytest
from app.lexer import lex_command

# test lexer
@pytest.mark.parametrize(
    "command, expected",
    [
        pytest.param("", [], id="empty-token"),
        pytest.param("echo ''", ["echo", ""], id="echo-empty-token"),
        pytest.param("echo '' ''", ["echo","",""], id="two-empty-tokens"),
        pytest.param("echo hello world", ["echo", "hello", "world"], id="hello-world"),
        pytest.param("echo 'hello world'", ["echo", "hello world"], id="single-quote"),
        pytest.param('echo "hello world"', ["echo", "hello world"], id="double-quote"),
        pytest.param(r"echo hello\ world", ["echo", "hello world"], id="ignore-backslash"),
        pytest.param(r"echo \\", ["echo", "\\"], id="echo-backslash"),
        pytest.param(r"echo \\\\", ["echo", "\\\\"], id="two-backslashes"),
        pytest.param("echo 'a\\b'", ["echo", "a\\b"], id="escape-backslash"),
        pytest.param("echo 'hello'world", ["echo", "helloworld"], id="no-separation"),
    ],
)
def test_lex_command(command, expected):
    assert lex_command(command) == expected