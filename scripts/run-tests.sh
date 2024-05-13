#!/usr/bin/env bash

# Setup variables.
scripts_dir="$(dirname "$0")"
repo_dir="$(dirname "$scripts_dir")"
cd "$repo_dir" || exit 1
if [[ -z $VIRTUAL_ENV ]]; then
    source ./env/bin/activate
fi

# Run tests.
if [[ $1 == '-v' ]]; then
    python3 -m unittest -v
else
    python3 -m unittest -b
fi
