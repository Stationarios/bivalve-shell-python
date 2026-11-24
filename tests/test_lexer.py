"""
tests whether lexer correctly divides the tokens and assigns the right token kind
"""
import pytest
from app.lexer import lex_command, Token

# test lexer
@pytest.mark.parametrize(
    "command, expected",
    [
        # empty tokens
        pytest.param("", [], id="empty-token"),
        pytest.param("echo ''", [Token("echo"), Token("")], id="echo-empty-token"),
        pytest.param("echo '' ''", [Token("echo"), Token(""), Token("")], id="two-empty-tokens"),
        # quoting
        pytest.param("echo hello world", [Token("echo"), Token("hello"), Token("world")], id="hello-world"),
        pytest.param("echo 'hello world'", [Token("echo"), Token("hello world")], id="single-quote"),
        pytest.param('echo "hello world"', [Token("echo"), Token("hello world")], id="double-quote"),
        pytest.param("echo 'hello'world", [Token("echo"), Token("helloworld")], id="no-separation"),
        # properly escaping
        pytest.param(r"echo hello\ world", [Token("echo"), Token("hello world")], id="ignore-backslash"),
        pytest.param(r"echo \\", [Token("echo"), Token("\\")], id="echo-backslash"),
        pytest.param(r"echo \\\\", [Token("echo"), Token("\\\\")], id="two-backslashes"),
        pytest.param("echo 'a\\b'", [Token("echo"), Token("a\\b")], id="escape-backslash"),
        # redirecting and NOT redirecting
        pytest.param("echo hi > out", [Token("echo"), Token("hi"), Token(">", "REDIRECT"), Token("out")], id="normal-redirect"),
        pytest.param("echo hi>out", [Token("echo"), Token("hi"), Token(">", "REDIRECT"), Token("out")], id="no-space-redirect"),
        pytest.param("echo hi 1> out", [Token("echo"), Token("hi"), Token("1>", "REDIRECT"), Token("out")], id="redirect-1>"),
        pytest.param("echo 1>out", [Token("echo"), Token("1>", "REDIRECT"), Token("out")], id="no-space-1>"),
        pytest.param(r"echo \1> out", [Token("echo"), Token("1"), Token(">", "REDIRECT"), Token("out")], id="escape-1"),
        pytest.param("echo ''>out", [Token("echo"), Token(""), Token(">", "REDIRECT"), Token("out")], id="redirect-empty"),
        pytest.param("echo '>' out", [Token("echo"), Token(">"), Token("out")], id=">-single-quote"),
        pytest.param('echo ">" out', [Token("echo"), Token(">"), Token("out")], id=">-double-quote"),
        pytest.param("echo 1>", [Token("echo"), Token("1>", "REDIRECT")], id="1>redirect-at-end"),
        pytest.param("echo >", [Token("echo"), Token(">", "REDIRECT")], id="redirect-at-end"),
        pytest.param("echo \>", [Token("echo"), Token(">")], id="escape-redirect"),
        pytest.param("echo '\>'", [Token("echo"), Token("\>")], id="quoted-escape-redirect"),
    ],
)
def test_lex_command(command, expected):
    assert lex_command(command) == expected