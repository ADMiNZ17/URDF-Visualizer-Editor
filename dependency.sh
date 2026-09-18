#!/bin/bash

# 1. Update package lists and install required system dependencies
echo "Checking system dependencies (you may be prompted for your sudo password)..."
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip zenity

# 2. Define the virtual environment directory name
VENV_DIR="venv"

# 3. Create the virtual environment if it doesn't already exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in ./$VENV_DIR..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

# 4. Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# 5. Upgrade pip and install Python requirements
echo "Installing Python dependencies (matplotlib, numpy)..."
pip install --upgrade pip
pip install matplotlib numpy

echo ""
echo "=================================================="
echo "Setup complete. To run your script, type:"
echo "source $VENV_DIR/bin/activate"
echo "python3 mplot3d.py"
echo "=================================================="