#!/bin/bash

# Get the directory location of the script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
ARGS=$@
cd $SCRIPT_DIR && ".venv/bin/python3" ykat.py "$@"
