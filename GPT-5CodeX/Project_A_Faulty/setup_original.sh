#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
# Activate the virtual environment (Windows-compatible path)
source .venv/Scripts/activate

python -m pip install --upgrade pip
python -m pip install -r requirements_original.txt
