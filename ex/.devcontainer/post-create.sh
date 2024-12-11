#!/bin/sh

# Upgrade pip
pip install --upgrade pip

# Install the package
pip install --user --editable ".[dev]"

# Install pre-commit
pre-commit install
