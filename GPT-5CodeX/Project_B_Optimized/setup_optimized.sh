#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/Scripts/activate

python -m pip install --upgrade pip
python -m pip install -r requirements_optimized.txt
