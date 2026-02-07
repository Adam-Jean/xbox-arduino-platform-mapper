#!/bin/bash
# Platform Controller launcher for Mac/Linux

echo "Platform Controller Launcher"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        echo "Please ensure Python 3.7+ is installed"
        exit 1
    fi
    echo ""
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
    echo ""
    echo "Setup complete!"
    echo ""
else
    source venv/bin/activate
fi

echo "Starting Platform Controller..."
echo ""
python main.py
