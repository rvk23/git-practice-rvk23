[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/PU2dD5kC)
# Project 3


This project uses the `lexer` and `parser` functions from Project 1 and Project 2 to get an instance of a `DatalogProgram` that must then be interpreted to answer its queries. Project 3 must

  1. Create a relation for each named scheme in the Datalog program.
  1. Add each fact in the Datalog program to the appropriate relation.
  1. Evaluate each query in the Datalog program and return the answers to each one.

**There is no rule evaluation for project 3.** Anything related to evaluating rules, including the natural join of two relations, is **not a part of project 3.**

The interpreter **must be implemented with relational algebra.** No exceptions. And the queries must be evaluated using relational algebra. Specifically, project, rename, and select along with union, intersection, and difference as appropriate.

**Before proceeding further, please review the Project 3 project description, lecture slides, and all of the associated Jupyter notebooks. You can thank us later for the suggestion.**

## Developer Setup

Be sure to read the [WARNING](#warning) and [Copy Files](#copy-files) sections.

As in Project 2, the first step is to clone the repository created by GitHub Classroom when the assignment was accepted in a sensible directory. In the vscode terminal, `git clone <URL>` where `<URL>` is the one from GitHub Classroom after accepting the assignment. Or open a new vscode window, select _Clone Git Repository_, and paste the link they get when they hover over the "<> Code ▼" and copy the url

There is no need to install any vscode extensions. These should all still be present and active from the previous project. You do need to create the virtual environment, install the package, and install pre-commit. For a reminder to how that is done, see on [learningsuite.byu.edu](https://learningsuite.byu.edu) _Content_ &rarr; _Projects_ &rarr; _Projects Cheat Sheet_

  * Create a virtual environment: **be sure to create it in the `project-3` folder.** `python -m venv .venv`
  * Activate the virtual environment: `source .venv/bin/activate` or `.venv\Scripts\activate` for OSX and windows respectively.
  * Install the package in edit mode: `pip install --editable ".[dev]"`
  * Install pre-commit: `pre-commit install`

The above should result in a `project3` executable that is run from the command line in an integrated terminal. As before, be sure the integrated terminal is in the virtual environment.

### WARNING

  * Be sure that the `conda` environment is not active when setting up the project. It's active when there is a `(base)` annotation next to the terminal prompt. The `conda deactivate` command will exit that environment.
  * Be sure the Python version is at least 3.11 -- `python --version`.
  * Open the project folder in vscode when working on the project, and not a folder above it or below it, otherwise the paths for the pass-off tests will not work -- the common error is _"no project3 module found"_.
  * Be sure that vscode is using the virtual environment in the project folder: choose `Python Select Interpreter` from the command pallette and select the Python in the `.venv` folder -- its usually the first option if vscode opened that folder as the workspace.

## Files

  * `.devcontainer`: container definition for those using docker with vscode
  * `.github`: workflow definitions
  * `README.md`: overview and directions
  * `config_test.sh`: support for auto-grading -- **please do not edit**
  * `pyproject.toml`: package definition and project configuration -- **please do not edit**
  * `pytest.ini`: custom pytest marks for pass-off -- **please do not edit**
  * `src`: folder for the package source files
  * `tests`: folder for the package test files
  * `.gitignore`: files patterns that git should ignore

### Copy Files

Copy the below files from your solution to Project 2 into the `src/project3/` folder:

  * `datalogprogram.py`
  * `fsm.py`
  * `lexer.py`
  * `parser.py`

The `token.py` file is unchanged here and should not be copied over. None of test files from Project 1 should be copied over either.

### Reminder

Please do not edit any of the following files or directories as they are related to _auto-grading_ and _pass-off_:

  * `config_test.sh`
  * `pytest.ini`
  * `./tests/test_passoff.py`
  * `./tests/resources/project3-passoff/*`

## Overview

The project is divided into the following modules each representing a key component of the project:

  * `src/project3/interpreter.py`: defines the `Interpreter` class with its interface.
  * `src/project3/project3.py`: defines the entry point for auto-grading and the command line entry point.
  * `src/project3/relation.py`: defines the `Relation` class with its interface.
  * `src/project3/reporter.py`: defines functions for reporting the results of the interpreter.

Each of the above files are specified with Python _docstrings_ and they also have examples defined with python _doctests_. A _docstring_ is a way to document Python code so that the command `help(project3.relation)` in the Python interpreter outputs information about the module with it's functions and classes. For functions, the docstrings give documentation when the mouse hovers over the function in vscode.

### interpreter.py

A portion of the `Interpreter` class needs to be implemented for project 3: `eval_schemes`, `eval_facts`, and `eval_queries`. The docstrings describe what
each should do. Relation algebra must be used for `eval_queries`. There are no provided tests. You are expected to write tests for each function before starting any implementation. Be sure to add to the repository the file with the tests.

### project3.py

The entry point for the auto-grader and the `project3` command. See the docstrings for details.

### relation.py

Some of the `Relation` class is already implemented. The attributes are complete as is the interface. A portion of the `Relation` class needs to be implemented for project 3: `intersection` (easy), `project` (hard), `rename` (super easy), `select_eq_col` (moderate), `select_eq_lit` (moderate), and `union` (easy). **You do not need natural join for project 3**.

The docstrings describe what each function should do. There are tests in `./tests/test_relation.py` for the provided portions of the class that are implemented already. You are expected to write negative and positive tests for each function before starting any implementation. A negative test is one where an error is expected (e.g., bad operands to an operation). Follow the examples provided in the test file.

### reporter.py

A module for output matching in the pass-off tests. It takes the interface defined by `Interpreter` and converts the return types to strings that are used for the actual query reports that must output match for pass-off. _This module should work out of the box and not need to be touched_.

## Where to start

Here is the suggested order for Project 3:

1. Read the code and order in your mind what has been provided, how it works, and what you need to implement -- **don't skip this step**.
1. For each required function in `Relation`:

    1. Write a negative test that fails.
    1. Write code to pass the negative test.
    1. Write a positive test that fails.
    1. Write code to pass the positive test.

1. For each required function in `Interpreter`:

    1. Write a positive test that fails.
    1. Write code to pass the positive test.

1. Run the pass-off tests -- debug as needed.

## Pass-off and Submission

**The pass-off test structure has changed.** All the tests are in a single file: `tests/test-passoff.py`. Running individual tests is the same using either `pytest` directly or the testing pane in vscode (**recommended**).

The minimum standard for this project is **bucket 80**. That means that if all the tests pass in all buckets up to and including bucket 80, then the next project can be started safely.

The Project 3 submission follows that of the other projects:

  * Commit your solution on the master branch -- be sure to add any new files!
  * Push the commit to GitHub -- that should trigger the auto-grader
  * Goto [learningsuite.byu.edu](https://learningsuite.byu.edu) at _Assignments_ &rarr; _Projects_ &rarr; _Project 3_ to submit your GitHub ID and Project 3 URL for grading.
  * Goto the Project 3 URL, find the green checkmark or red x, and click it to confirm the auto-grader score matches the pass-off results from your system.

### Branches

Consider using a branch as you work on your submission so that you can `commit` your work from time to time. Once everything is working, and the auto-grader tests are passing, then you can `merge` your work into your master branch and push it to your GitHub repository. Ask your favorite search engine or LLM for help learning how to use Git feature branches.
