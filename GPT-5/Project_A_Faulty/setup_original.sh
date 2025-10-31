#!/usr/bin/env bash
set -e
python -m venv .venv_original
source .venv_original/Scripts/activate || source .venv_original/bin/activate
pip install -r requirements_original.txt
echo "Environment ready (faulty project)."