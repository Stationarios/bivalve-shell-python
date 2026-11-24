This repo is based on the "build your own shell" challenge from CodeCrafters. This repo is mainly written in Python.  
The name of this shell is **bivalve**.  

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# How to run the bivalve shell
Clone this repo. Just `bash your_program.sh` or `./your_program.sh` to run bivalve.

# How to run tests
There are two tests currently, one for testing the lexer, another for the shell.  
Use `uv run python -m pytest` to run all the tests. Use `uv run python -m pytest -v` to see the details of each test.

# What has been done (and not done yet)
- Stage 1: Usable commands include: `exit`, `echo` and `type`. Executables can also be run.
- Stage 2: `pwd` and `cd` are added. Can change directory.
- Stage 3: Quoting implemented. Single and double quotes are added. Backslashes are (partly) working.
*Not all special characters are dealt with yet.*
- Stage 4: Redirection being implemented. Redirection of `stdout` is working.
*Other stuff not yet.*
- Basic scripts for automated testing is created based on pytest.
*Testing cases still need to be sorted out to keep up with the shell.*

# What's next
- Command completion
- Filename completion
- Programmable completion
- Background jobs
- Pipelines
- History
- History persistence
- Parameter expansion
- Constantly checking out the bash reference manual to find out extra stuff I've missed
- More DIY stuff I'm considering (e.g. bivalve shell with "evil output" style...?)