#!/bin/bash

# Set up a Python virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found! Please provide one."
fi

echo "✅ Setup complete! Use 'source venv/bin/activate' to activate the environment."
