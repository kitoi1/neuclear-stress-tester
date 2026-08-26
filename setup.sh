#!/bin/bash

set -e

echo "🚀 Setting up Nuclear Stress Tester..."

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing package and development dependencies..."
python -m pip install -e ".[dev]"

echo "🔧 Installing pre-commit hooks..."

if command -v pre-commit >/dev/null 2>&1; then
    pre-commit install
else
    echo "⚠️ pre-commit was not found."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Activate manually with:"
echo "  source venv/bin/activate"
echo ""
echo "Test installation:"
echo "  neuclear --help"
echo ""
echo "Run tests:"
echo "  pytest"