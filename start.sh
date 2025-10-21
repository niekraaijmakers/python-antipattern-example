#!/bin/bash

# Quick start script for the anti-pattern example

echo "🚫 Starting the TERRIBLE Web Application Example 🚫"
echo "=================================================="
echo ""
echo "⚠️  WARNING: This is intentionally bad code!"
echo "    Do NOT use these patterns in real projects!"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Flask not found. Installing requirements..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "✓ Flask is installed"
echo ""

# Remove old database if exists
if [ -f "students.db" ]; then
    echo "🗑️  Removing old database..."
    rm students.db
fi

echo "🚀 Starting the server..."
echo "📍 Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 terrible_server.py

