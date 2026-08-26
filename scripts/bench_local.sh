#!/bin/bash

set -e

echo "🚀 Starting Nuclear Stress Tester Benchmark"
echo "=========================================="

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python3 is not installed."
    exit 1
fi

if ! command -v pip >/dev/null 2>&1; then
    echo "❌ pip is not installed."
    exit 1
fi

echo "📦 Installing package..."
python3 -m pip install -e .

echo "🔧 Testing installation..."
neuclear --help

TEST_DIR="benchmark_results"

mkdir -p "$TEST_DIR"

echo "🧪 Running benchmark scenarios..."

echo "1. Light load..."

neuclear test http://localhost:8080 \
    --workers 1 \
    --rate 10 \
    --duration 10s \
    --output "$TEST_DIR/light_test.json" \
    --quiet

echo "2. Medium load..."

neuclear test http://localhost:8080 \
    --workers 2 \
    --rate 50 \
    --duration 30s \
    --output "$TEST_DIR/medium_test.json" \
    --quiet

echo "3. Heavy load..."

neuclear test http://localhost:8080 \
    --workers 4 \
    --rate 100 \
    --duration 60s \
    --output "$TEST_DIR/heavy_test.json" \
    --quiet

echo ""
echo "✅ All benchmarks completed!"
echo "📊 Results saved in: $TEST_DIR/"