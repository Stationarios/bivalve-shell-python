import sys
import os
import subprocess

BUILTINS = {"echo", "exit", "type"}

def find_executable(name : str) -> str | None:
    dir_paths = os.environ.get("PATH", "").split(os.pathsep)

    for dir_path in dir_paths:
        file_path = os.path.join(dir_path, name)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path

    return None

def run_executable(command : str) -> None:
    parts = command.split()
    if not parts:
        pass
    name = parts[0]
    args = parts[1:]

    executable = find_executable(name)
    if executable is not None:
        subprocess.run([executable, *args])
    else:
        print(f"{name}: command not found")

def handle_type(name : str) -> None:
    if name in BUILTINS:
        print(f"{name} is a shell builtin")
    elif(find_executable(name) != None):
        print(f"{name} is {find_executable(name)}")
    else:
        print(f"{name}: not found")

def main():
    while True:
        sys.stdout.write("$ ")
        try:
            command = input()
        except EOFError:
            break
        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            command_name = command[5:]
            handle_type(command_name)
        else:
            run_executable(command)
    # pass


if __name__ == "__main__":
    main()
