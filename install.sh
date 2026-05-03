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


#  VSCode (ipynb)
#
#   - Дебаг (launch.json)
#   - Кнопки запуска (tasks.json)
#
#  "Debug Console" в VSCode!
#
#   Когда ставишь breakpoint и останавливаешься,
#   можно выполнять Python-команды прямо в
#   контексте текущего состояния программы.

# PYTHONPATH
#
# case ":$PYTHONPATH:" in
#     *":$PROJ:"*) ;;
#     *) export PYTHONPATH=\
#         "$PROJ${PYTHONPATH:+:$PYTHONPATH}" ;;
# esac
