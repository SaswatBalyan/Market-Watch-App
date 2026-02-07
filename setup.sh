#!/bin/bash
# Quick Setup & Launch Script for Market Watch Dashboard

set -e

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "Checking Python installation..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "Python not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo "Found: $PYTHON_VERSION"
echo ""

# Check if we're in the right directory
if [ ! -f "data_handler.py" ]; then
    echo "Error: data_handler.py not found"
    echo "Please run this script from the 95USStock directory:"
    echo "  cd /home/saswat-balyan/devStuff/95USStock"
    echo "  bash setup.sh"
    exit 1
fi

echo " Project directory: $(pwd)"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "   (This may take 1-2 minutes)"
echo ""

if ! $PYTHON_CMD -m pip install -q -r requirements.txt; then
    echo "Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully"
echo ""

# Verify installation
echo "Verifying installation..."
if $PYTHON_CMD -c "import pandas, plotly, streamlit; print('All required packages loaded')" 2>/dev/null; then
    echo ""
else
    echo "Some packages failed to load"
    exit 1
fi


if $PYTHON_CMD test_market_watch.py 2>&1 | tail -15; then
    echo ""
    echo "All tests passed!"
else
    echo ""
    echo " Some tests failed, but continuing..."
fi
echo "To start the dashboard, run:"
echo ""
echo "    streamlit run app.py"
echo ""
echo "The app will open at:  http://localhost:8501"
