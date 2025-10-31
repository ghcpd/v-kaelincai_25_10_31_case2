#!/usr/bin/env bash
set -e
python -m venv .venv_optimized
source .venv_optimized/Scripts/activate || source .venv_optimized/bin/activate
pip install -r requirements_optimized.txt
echo "Environment ready (optimized project)."