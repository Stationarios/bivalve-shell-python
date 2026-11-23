"""
lexer for shell commands.
"""

def lex_command(command: str) -> list[str]:
    tokens = []
    current = []
    quote = None # quote is either None, ' or "
    token_started = False

    i = 0
    while i < len(command):
        c = command[i]
        if c == "\\":
            if quote == None or (
                quote == '"' and i + 1 < len(command)
                and command[i + 1] in '$`"\\'
            ):
                if i + 1 >= len(command):
                    print("bivalve: isolated backslash at the end")
                    return []
                token_started = True
                current.append(command[i + 1])
                i += 1
            else:
                current.append(c)
                token_started = True
        elif c in ("'", '"'):
            if quote is None:
                quote = c
                token_started = True
            elif quote == c:
                quote = None
            else:
                current.append(c)
        elif c == " ":
            if quote is not None:
                current.append(c)
            elif quote == None and token_started == True:
                token_started = False
                tokens.append("".join(current))
                current = []
        else:
            current.append(c)
            token_started = True

        i += 1

    if quote is not None:
        print("bivalve: unmatched quote")
        return []

    if token_started == True:
        tokens.append("".join(current))

    return tokens
