#!/usr/bin/env bash

script_dir="$(dirname "$0")"
repo_dir="$(dirname "$script_dir")"
cd "${repo_dir}/docs" || exit 1

if [[ $1 == '-c' || $1 == '--clean' ]]; then
    make clean
fi

make html
