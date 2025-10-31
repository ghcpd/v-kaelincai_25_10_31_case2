#!/bin/bash

echo "========================================="
echo "Setting up Project A - Faulty Implementation"
echo "========================================="

# Create virtual environment
python -m venv venv_original

# Activate virtual environment (platform-specific)
if [ -f "venv_original/Scripts/activate" ]; then
    # Windows
    source venv_original/Scripts/activate
else
    # Linux/Mac
    source venv_original/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements_original.txt

echo ""
echo "Setup complete for Project A!"
echo "Environment: venv_original"
echo "========================================="
