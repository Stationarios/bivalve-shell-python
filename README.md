This repo is based on the "build your own shell" challenge from CodeCrafters. This repo is mainly written in Python.  
The name of this shell is bivalve.  

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# how to run the bivalve shell
Clone this repo. Just `bash your_program.sh` or `./your_program.sh` and it'll be up and running.

# how to run tests
There are two tests currently, one for testing the lexer, another for the shell.  
Use `uv run python -m pytest` to run all the tests. Use `uv run python -m pytest -v` to see the details of each test.

# what has been done
- Stage 1: Usable commands include: `exit`, `echo` and `type`. Executables can also be run.
- Stage 2: `pwd` and `cd` are added. Can change directory.
- A basic script for automated testing is created based on pytest.

# what's next
- quoting
- redirection
- command completion
- filename completion
- programmable completion
- background jobs
- pipelines
- history
- history persistence
- parameter expansion
- more DIY stuff I'm considering...