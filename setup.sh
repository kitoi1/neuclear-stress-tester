#!/usr/bin/env bash

set -euo pipefail

echo "🚀 Setting up Nuclear Stress Tester..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

echo "🐍 Python version: $PYTHON_VERSION"

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

echo "📦 Installing Nuclear Stress Tester and development dependencies..."
python -m pip install -e ".[dev]"

if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
fi

echo ""
echo "✅ Setup complete!"
echo ""

echo "CLI:"
echo "  neuclear --help"
echo ""

echo "Run tests:"
echo "  pytest"
echo ""

echo "Activate environment:"
echo "  source venv/bin/activate"
echo ""

echo "Run a SAFE local test:"
echo "  neuclear test http://localhost:8080 --workers 1 --rate 10 --duration 10s"
echo ""
