#!/bin/bash

PROJ="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJ"

[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
    python -m pip install -r requirements.txt
    python -m pip install ipykernel
    python -m ipykernel install --user --name\
        alg2 --display-name "Python (alg2)"
deactivate


# ~/.bashrc
#
# cd() {
#     builtin cd "$@"
#     if [ -f .venv/bin/activate ]; then
#         source .venv/bin/activate
#         export PYTHONPATH="$PWD"
#     elif [ -n "$VIRTUAL_ENV" ]; then
#         deactivate
#         export PYTHONPATH=""
#     fi
# }
