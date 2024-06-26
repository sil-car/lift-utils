#!/usr/bin/env bash

script_dir="$(dirname "$0")"
repo_dir="$(dirname "$script_dir")"
cd "${repo_dir}/sphinx" || exit 1

if [[ $1 == '-c' || $1 == '--clean' ]]; then
    # clean before building
    make clean
    # rm -f "${repo_dir}/docs"*
fi

make html
# sphinx-build "${repo_dir}/sphinx/source" "${repo_dir}/docs"
