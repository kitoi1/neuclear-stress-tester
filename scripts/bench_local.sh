#!/bin/bash
# Benchmark script for local testing

set -e

echo "🚀 Starting Nuclear Stress Tester Benchmark"
echo "=========================================="

# Check if Python and pip are installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Install the package in development mode
echo "📦 Installing package in development mode..."
pip install -e .

# Run the CLI help to verify installation
echo "🔧 Testing installation..."
neuclear --help

# Create test directory
TEST_DIR="benchmark_results"
mkdir -p "$TEST_DIR"

# Run different test scenarios
echo "🧪 Running benchmark scenarios..."

# Light load test
echo "1. Running light load test..."
neuclear test http://localhost:8080 \
  --processes 2 \
  --rate 100 \
  --duration 10s \
  --output "$TEST_DIR/light_test.json" \
  --quiet

# Medium load test
echo "2. Running medium load test..."
neuclear test http://localhost:8080 \
  --processes 4 \
  --rate 200 \
  --duration 15s \
  --output "$TEST_DIR/medium_test.json" \
  --quiet

# Heavy load test
echo "3. Running heavy load test..."
neuclear test http://localhost:8080 \
  --processes 8 \
  --rate 500 \
  --duration 10s \
  --output "$TEST_DIR/heavy_test.json" \
  --quiet

echo "✅ All benchmarks completed!"
echo "📊 Results saved in: $TEST_DIR/"
echo ""
echo "To view results:"
echo "  cat $TEST_DIR/light_test.json | python -m json.tool"
echo ""
echo "To clean up:"
echo "  rm -rf $TEST_DIR/"