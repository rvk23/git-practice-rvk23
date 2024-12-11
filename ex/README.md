[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/OUI2GsPt)
# Project 4


This project uses the `lexer` and `parser` functions from Project 1 and Project 2 to get an instance of a `DatalogProgram`. It also uses the `Interpreter.eval_schemes`, `Interpreter.eval_facts`, and `Interpreter.eval_queries` from Project 3. Project 4 must evaluate the rules in the Datalog program to add new facts to relations that exist in the database. This will be done by implementing the `Interpreter.eval_rule` function according to the algorithm specified in the project description on [learningsuite.byu.edu](http://learningsuite.byu.edu) in the _Content_ section under _Projects_ -> _Project 4_.

The rule evaluation **must be implemented with relational algebra.** No exceptions. Rule evaluation should re-use the existing code for `Interpreter.eval_query` from Project 3 to create intermediate relations.

Why do we use `Interpreter.eval_query` for evaluating rules? Consider this example rule: `R(X,Z) :- G(X,Y,'a'), R(Y,Z).` To evaluate this rule, we need to first compute the operands to the _join_ operation. The left operand is given by `G(X,Y,'a')` and the right operand is given by `R(Y,Z)`. Assuming that the relations are declared in the _Schemes_ section of the Datalog program as `G(A,B,C)` and `R(A,B)` respectively, then the relation for the left operand is `left = rename([X,Y], project([A,B], (select(C = 'a', G)))` and the relation for the right operand is `right = rename([Y,Z], project([A,B], R))`. These two operands are **the resulting relations when each operand is treated as a query**.

The `,` in the rule represents join. The head predicate in our rule, `R(X,Z)`, tells us how to format the final relation from the join: `project([X,Z], join(left, right))`. The tuples in this final relation are added to the relation `R` in the database. That may require a rename operation to use `Relation.union`. Rules are evaluated, in order, until no new facts are added to any of the relations in the database. The `Relation.union` relational operator must be used for Project 4. Whether you implemented union in Project 3 or will implement it in Project 4, you should include unit tests for this operation.

**Before proceeding further, please review the Project 4 project description, lecture slides, and all of the associated Jupyter notebooks. You can thank us later for the suggestion.**

## Developer Setup

Be sure to read the [WARNING](#warning) and [Copy Files](#copy-files) sections.

As in Project 3, the first step is to clone the repository created by GitHub Classroom when the assignment was accepted in a sensible directory. In the vscode terminal, `git clone <URL>` where `<URL>` is the one from GitHub Classroom after accepting the assignment. Or open a new vscode window, select _Clone Git Repository_, and paste the link they get when they hover over the "<> Code ▼" and copy the url

There is no need to install any vscode extensions. These should all still be present and active from the previous project. You do need to create the virtual environment, install the package, and install pre-commit. For a reminder to how that is done, see on [learningsuite.byu.edu](https://learningsuite.byu.edu) _Content_ &rarr; _Projects_ &rarr; _Projects Cheat Sheet_

  * Create a virtual environment: **be sure to create it in the `project-4` folder.** `python -m venv .venv`
  * Activate the virtual environment: `source .venv/bin/activate` or `.venv\Scripts\activate` for OSX and windows respectively.
  * Install the package in edit mode: `pip install --editable ".[dev]"`
  * Install pre-commit: `pre-commit install`

The above should result in a `project4` executable that is run from the command line in an integrated terminal. As before, be sure the integrated terminal is in the virtual environment.

### WARNING

  * Be sure that the `conda` environment is not active when setting up the project. It's active when there is a `(base)` annotation next to the terminal prompt. The `conda deactivate` command will exit that environment.
  * Be sure the Python version is at least 3.11 -- `python --version`.
  * Open the project folder in vscode when working on the project, and not a folder above it or below it, otherwise the paths for the pass-off tests will not work -- the common error is _"no project4 module found"_.
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

Copy the below files from your solution to Project 3 into the `src/project4/` folder:

  * `datalogprogram.py`
  * `fsm.py`
  * `interpreter.py`
  * `lexer.py`
  * `parser.py`
  * `relation.py`
  * `./tests/test_relation.py`
  * `./tests/test_interpreter.py`

The `token.py` file is unchanged here and should not be copied over. Other test files from older projects can be copied as needed.

### Reminder

Please do not edit any of the following files or directories as they are related to _auto-grading_ and _pass-off_:

  * `config_test.sh`
  * `pytest.ini`
  * `./tests/test_passoff.py`
  * `./tests/resources/project4-passoff/*`

## Overview

The project is divided into the following modules each representing a key component of the project:

  * `src/project4/interpreter.py`: defines the `Interpreter` class with its interface.
  * `src/project4/project4.py`: defines the entry point for auto-grading and the command line entry point.
  * `src/project4/relation.py`: defines the `Relation` class with its interface.
  * `src/project4/reporter.py`: defines functions for reporting the results of the interpreter.

Each of the above files are specified with Python _docstrings_ and they also have examples defined with python _doctests_. A _docstring_ is a way to document Python code so that the command `help(project4.relation)` in the Python interpreter outputs information about the module with it's functions and classes. For functions, the docstrings give documentation when the mouse hovers over the function in vscode.

### interpreter.py

The portion of the `Interpreter` class that needs to be implemented for Project 4 is `eval_rules`. The docstring describe what
it should do. There are no provided tests. You are expected to write tests for the function before starting any implementation. There should a few tests that cover interesting inputs for rule evaluation. Justify why the set of tests are sufficient to give confidence in the implementation.

### project4.py

The entry point for the auto-grader and the `project4` command. See the docstrings for details.

### relation.py

The only part of the `Relation` class that needs to be implemented for Project 4 is `join` (hard). The docstring describe what the function should do. **You are expected to write one negative test for `join` and at least three positive tests: one for when there are no shared attributes, one for when all the attributes are shared, and one from when the is a mix of each.**

You are expected to write one test, run it to see what happens (likely fail), and then write the code to pass that one test. Repeat the process for each test. As before, a negative test is one where an error is expected (e.g., bad operands to an operation).

The `Relation.union` relational operator must be used for Project 4. Whether you implemented union in Project 3 or will implement it in Project 4, you should include unit tests for this operation.

### reporter.py

A module for output matching in the pass-off tests. It takes the interface defined by `Interpreter` and converts the return types to strings that are used for the actual query reports that must output match for pass-off. _This module should work out of the box and not need to be touched_.

## Where to start

Here is the suggested order for Project 4:

1. Write a negative test that fails for `Relation.join`.
1. Write code to pass the negative test.

1. For a set of interesting inputs for `Relation.join` -- you must consider at least three unique tests: no shared attributes, attributes shared, and a mix of shared and not shared attributes:

    1. Write a positive test that may fail (should fail the first test because no code has been written and may fail other tests depending on the code written for the first test).
    1. Write code to pass the positive test.

1. For a set of interesting inputs for `Interpreter.eval_rules` -- as a starting point consider if number of iterations to reach a fix-point matters in testing or if the number of rules being evaluated matters:

    1. Write a positive test that may fail (should fail the first test because no code has been written and may fail other tests depending on the code written for the first test).
    1. Write code to pass the positive test.

1. Run the pass-off tests -- debug as needed.

## Pass-off and Submission

All the pass-off tests are in a single file: `tests/test-passoff.py`. Running individual tests is the same using either `pytest` directly or the testing pane in vscode (**recommended**).

The minimum standard for this project is **bucket 80**. That means that if all the tests pass in all buckets up to and including bucket 80, then the next project can be started safely.

The Project 4 submission follows that of the other projects:

  * Commit your solution on the master branch -- be sure to add any new files!
  * Push the commit to GitHub -- that should trigger the auto-grader
  * Goto [learningsuite.byu.edu](https://learningsuite.byu.edu) at _Assignments_ &rarr; _Projects_ &rarr; _Project 4_ to submit your GitHub ID and Project 4 URL for grading.
  * Goto the Project 4 URL, find the green checkmark or red x, and click it to confirm the auto-grader score matches the pass-off results from your system.

### Branches

Consider using a branch as you work on your submission so that you can `commit` your work from time to time. Once everything is working, and the auto-grader tests are passing, then you can `merge` your work into your master branch and push it to your GitHub repository. Ask your favorite search engine or LLM for help learning how to use Git feature branches.
