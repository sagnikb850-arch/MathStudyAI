#!/bin/bash

# Math Study AI - Linux/Mac Startup Script

echo ""
echo "========================================"
echo "  Math Study AI - Startup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
fi

# Activate venv
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "[3/4] Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "[WARNING] .env file not found!"
    echo "Please copy .env.example to .env and add your API key"
    echo ""
    echo "Example:"
    echo "  - Copy: cp .env.example .env"
    echo "  - Edit: nano .env and add OPENAI_API_KEY=sk-..."
    echo ""
fi

# Start backend
echo "[4/4] Starting Math Study AI Backend..."
echo ""
echo "Starting server on http://localhost:5000"
echo "Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python app.py
