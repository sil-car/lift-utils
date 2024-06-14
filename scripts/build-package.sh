#!/usr/bin/env bash

# Setup variables.
scripts_dir="$(dirname "$0")"
repo_dir="$(dirname "$scripts_dir")"
cd "$repo_dir" || exit 1
if [[ -z $VIRTUAL_ENV ]]; then
    # shellcheck disable=SC1091
    source ./env/bin/activate
fi

rm -rf dist/*
python3 -m build
