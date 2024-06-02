#!/bin/sh

flake8
isort --check .
black --check .
mypy .