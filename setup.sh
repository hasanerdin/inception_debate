#!/bin/bash

echo "🚀 Setting up the project environment..."

# Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python 3.9+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup complete!"
echo "➡️ To activate the environment later, run:"
echo "   source venv/bin/activate"
echo "➡️ To deactivate, simply run:"
echo "   deactivate"
echo ""