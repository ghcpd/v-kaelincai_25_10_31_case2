#!/bin/bash

echo "========================================="
echo "Setting up Project B - Optimized Implementation"
echo "========================================="

# Create virtual environment
python -m venv venv_optimized

# Activate virtual environment (platform-specific)
if [ -f "venv_optimized/Scripts/activate" ]; then
    # Windows
    source venv_optimized/Scripts/activate
else
    # Linux/Mac
    source venv_optimized/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements_optimized.txt

echo ""
echo "Setup complete for Project B!"
echo "Environment: venv_optimized"
echo "========================================="
