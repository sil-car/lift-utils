#!/usr/bin/env bash

# Setup variables.
scripts_dir="$(dirname "$0")"
repo_dir="$(dirname "$scripts_dir")"
cd "$repo_dir" || exit 1
if [[ -z $VIRTUAL_ENV ]]; then
    source ./env/bin/activate
fi

python -m cProfile -s tottime -m unittest tests/test_lexicon_v0_13_FW.py
