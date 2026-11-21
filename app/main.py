import sys
import os
import subprocess
from app.lexer import lex_command

BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def handle_echo(args: list[str]) -> None:
    print(" ".join(args))

def find_executable(name: str) -> str | None:
    dir_paths = os.environ.get("PATH", "").split(os.pathsep)

    for dir_path in dir_paths:
        file_path = os.path.join(dir_path, name)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path

    return None

def handle_type(args: list[str]) -> None:
    if not args:
        print("type: missing argument")
        return
    
    for target in args:
        if target in BUILTINS:
            print(f"{target} is a shell builtin")
        elif(find_executable(target) != None):
            print(f"{target} is {find_executable(target)}")
        else:
            print(f"{target}: not found")

def run_executable(name: str, args: list[str]) -> None:
    executable = find_executable(name)
    if executable is not None:
        subprocess.run([executable, *args])
    else:
        print(f"{name}: command not found")

def handle_pwd() -> None:
    print(os.getcwd())

def handle_cd(args: list[str]) -> None:
    if len(args) > 1:
        print("cd: too many arguments")
        return
    path = args[0] if args else "~"
    path = os.path.expanduser(path)
    try:
        os.chdir(path)
    except OSError as e:
        print(f"cd: {path}: {e.strerror}")

def main():
    while True:
        sys.stdout.write("$ ")
        try:
            command = input()
        except EOFError:
            break

        parts = lex_command(command)
        if not parts:
            continue
        name = parts[0]
        args = parts[1:]

        if command == "exit":
            break
        elif name == "echo":
            handle_echo(args)
        elif name == "type":
            handle_type(args)
        elif name == "pwd":
            handle_pwd()
        elif name == "cd":
            handle_cd(args)
        else:
            run_executable(name, args)
    # pass

if __name__ == "__main__":
    main()
