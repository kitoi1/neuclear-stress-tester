#!/bin/bash

echo "🚀 Setting up Nuclear Stress Tester..."

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "📦 Installing package in development mode..."
pip install -e .

# Install development dependencies
echo "🔧 Installing development dependencies..."
pip install -e ".[dev]"

# Setup pre-commit hooks
echo "✅ Installing pre-commit hooks..."
pre-commit install

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment manually:"
echo "  source venv/bin/activate"
echo ""
echo "To test the installation:"
echo "  neuclear --help"
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To run a sample test:"
echo "  neuclear test https://httpbin.org/get --processes 2 --rate 10 --duration 5s"
