import sys
import os
import subprocess
from app.lexer import lex_command
from app.parser import parse_command

BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def handle_echo(args: list[str], out) -> None:
    print(" ".join(args), file = out)

def find_executable(name: str) -> str | None:
    dir_paths = os.environ.get("PATH", "").split(os.pathsep)

    for dir_path in dir_paths:
        file_path = os.path.join(dir_path, name)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path

    return None

def handle_type(args: list[str], out) -> None:
    if not args:
        print("type: missing argument", file = sys.stderr)
        return
    
    for target in args:
        if target in BUILTINS:
            print(f"{target} is a shell builtin", file = out)
        elif (path := find_executable(target)) is not None:
            print(f"{target} is {path}", file=out)
        else:
            print(f"{target}: not found", file = sys.stderr)

def run_executable(name: str, args: list[str], out) -> None:
    executable = find_executable(name)
    if executable is not None:
        subprocess.run([executable, *args], stdout = out)
    else:
        print(f"{name}: command not found", file = sys.stderr)

def handle_pwd(out) -> None:
    print(os.getcwd(), file = out)

def handle_cd(args: list[str]) -> None:
    if len(args) > 1:
        print("cd: too many arguments", file = sys.stderr)
        return
    path = args[0] if args else "~"
    path = os.path.expanduser(path)
    try:
        os.chdir(path)
    except OSError as e:
        print(f"cd: {path}: {e.strerror}", file = sys.stderr)

def main():
    while True:
        sys.stdout.write("$ ")
        try:
            user_input = input()
        except EOFError:
            break

        tokens = lex_command(user_input)
        command = parse_command(tokens)

        if command is None:
            continue

        name = command.parts[0]
        args = command.parts[1:]
        stdout_path = command.stdout_path

        # output
        out = None
        if stdout_path is not None:
            try:
                out = open(stdout_path, "w")
            except OSError as e:
                print(f"bivalve: {e}", file = sys.stderr)
                continue
        
        # commands
        try:
            if name == "exit":
                break
            elif name == "echo":
                handle_echo(args, out)
            elif name == "type":
                handle_type(args, out)
            elif name == "pwd":
                handle_pwd(out)
            elif name == "cd":
                handle_cd(args)
            else:
                run_executable(name, args, out)
        finally:
            if out is not None:
                out.close()

if __name__ == "__main__":
    main()
