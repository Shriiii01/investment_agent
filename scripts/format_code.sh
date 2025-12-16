#!/bin/bash
# Format code using black and isort

echo "Formatting Python code..."

# Check if black is installed
if ! command -v black &> /dev/null; then
    echo "Installing black..."
    pip install black
fi

# Check if isort is installed
if ! command -v isort &> /dev/null; then
    echo "Installing isort..."
    pip install isort
fi

# Format code
black *.py scripts/*.py tests/*.py
isort *.py scripts/*.py tests/*.py

echo "✅ Code formatting complete!"

