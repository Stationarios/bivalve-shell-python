"""
lexer for shell commands.
"""

def lex_command(command: str) -> list[str]:
    tokens = []
    current = []
    in_single_quote = False
    token_started = False
    for c in command:
        if c == "'":
            in_single_quote = not in_single_quote
            token_started = True
        elif c != " ":
            current.append(c)
            token_started = True
        elif c == " " and in_single_quote == True:
            current.append(c)
        elif c == " " and in_single_quote == False and token_started == True:
            token_started = False
            tokens.append("".join(current))
            current = []
    
    if token_started == True:
        tokens.append("".join(current))
    
    return tokens