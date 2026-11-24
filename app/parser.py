"""
parse commands properly for main.py
"""
import sys
from dataclasses import dataclass

@ dataclass
class Command:
    parts: list[str]
    stdout_path: str | None = None

def parse_command(tokens: list[Token] | None) -> Command | None:
    command = Command([])
    if tokens is None:
        return None
    i = 0
    while (i < len(tokens)):
        if (tokens[i].kind == "REDIRECT"):
            if i + 1 >= len(tokens):
                print("bivalve: syntax error near unexpected token `newline'", file = sys.stderr)
                return None
            elif tokens[i + 1].kind != "WORD":
                print(f"bivalve: syntax error near unexpected token `{tokens[i + 1].text}'", file = sys.stderr)
                return None
            else:
                command.stdout_path = tokens[i + 1].text
                i += 1
        else:
            command.parts.append(tokens[i].text)
        i += 1
    
    return command