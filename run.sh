#!/bin/bash

# Placement Prep Application - Run Script

echo "=========================================="
echo "Placement Prep Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null
then
    echo "❌ Python is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python"
if command -v python3 &> /dev/null
then
    PYTHON_CMD="python3"
fi

echo "Using: $PYTHON_CMD"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Check if database exists
if [ ! -f "placement_prep.db" ]; then
    echo "🗄️  Database not found. Initializing..."
    $PYTHON_CMD init_db.py
    echo ""
fi

# Run test
echo "🧪 Running setup tests..."
$PYTHON_CMD test_setup.py
echo ""

# Start application
echo "🚀 Starting Flask application..."
echo "=========================================="
echo "Open your browser and go to:"
echo "http://127.0.0.1:5000"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

$PYTHON_CMD app.py
