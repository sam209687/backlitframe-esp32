#!/bin/bash
# setup.sh
# One-time Ubuntu environment setup for Smart Showroom AI.
# Run from the project root: ./setup.sh

set -e

echo "== Smart Showroom AI setup =="

# 1. System packages needed for PySide6 / audio / opencv on Ubuntu
echo "Installing system dependencies (requires sudo password)..."
sudo apt update
sudo apt install -y \
    python3 python3-venv python3-pip python3-dev \
    build-essential \
    libgl1 \
    portaudio19-dev \
    ffmpeg

# 2. Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists, skipping creation."
fi

# 3. Activate and install Python dependencies
echo "Installing Python packages into venv..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "== Setup complete =="
echo "Next steps:"
echo "  source venv/bin/activate"
echo "  python database/init_db.py"
echo "  python main.py"
