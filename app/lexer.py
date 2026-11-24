"""
lexer for shell commands.
"""
import sys
from dataclasses import dataclass

# A token has its text and "kind". For now there are 2 kinds: "WORD" and "REDIRECT"
@dataclass
class Token:
    text: str
    kind: str = "WORD"

def lex_command(command: str) -> list[str] | None:
    tokens = []
    current = []
    quote = None # quote is either None, ' or "
    token_started = False
    is_quoted = False # true if there is any escape or quote in the current token

    i = 0
    while i < len(command): 
        c = command[i]
        if c == "\\":
            if quote == None or (
                quote == '"' and i + 1 < len(command)
                and command[i + 1] in '$`"\\'
            ):
                if i + 1 >= len(command):
                    print("bivalve: isolated backslash at the end", file = sys.stderr)
                    return None
                token_started = True
                is_quoted = True
                current.append(command[i + 1])
                i += 1
            else:
                current.append(c)
                token_started = True
        elif c in ("'", '"'):
            if quote is None:
                quote = c
                token_started = True
                is_quoted = True
            elif quote == c:
                quote = None
            else:
                current.append(c)
        elif c == ">":
            if quote is not None:
                current.append(c)
            else:
                if current == ["1"] and is_quoted == False:
                    tokens.append(Token("1>", "REDIRECT"))
                else:
                    if token_started == True:
                        tokens.append(Token("".join(current)))
                    tokens.append(Token(">", "REDIRECT"))
                
                current = []
                is_quoted = False
                token_started = False
        elif c == " ":
            if quote is not None:
                current.append(c)
            elif quote == None and token_started == True:
                token_started = False
                tokens.append(Token("".join(current)))
                current = []
                is_quoted = False
        else:
            current.append(c)
            token_started = True

        i += 1

    if quote is not None:
        print("bivalve: unmatched quote", file = sys.stderr)
        return None

    if token_started == True:
        tokens.append(Token("".join(current)))

    return tokens
