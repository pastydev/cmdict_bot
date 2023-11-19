#!/bin/sh
# Bash script to run Poetry to update dependencies and requirements files.

poetry update --with dev

poetry export -f requirements.txt --output requirements.txt --without-hashes
