#!/bin/bash
# Quick setup script for downloading IXI datasets

set -e

echo "=========================================="
echo "🧠 IXI Dataset Setup Script"
echo "=========================================="
echo ""

# Check if kaggle.json exists
if [ ! -f "kaggle.json" ]; then
    echo "❌ Error: kaggle.json not found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://www.kaggle.com/settings"
    echo "2. Scroll to 'API' section"
    echo "3. Click 'Create New API Token'"
    echo "4. Save the downloaded kaggle.json to this directory"
    echo ""
    exit 1
fi

echo "✓ Found kaggle.json"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python not found!"
    echo "Please ensure Python is installed and activated in your environment."
    exit 1
fi

echo "✓ Python is available"
echo ""

# Check if kaggle package is installed
if ! python -c "import kaggle" 2>/dev/null; then
    echo "⚠️  Kaggle package not found. Installing..."
    pip install kaggle
    echo ""
fi

echo "✓ Kaggle package is available"
echo ""

# Run the download script
echo "🚀 Starting dataset download..."
echo ""

python scripts/download_datasets.py "$@"

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="

