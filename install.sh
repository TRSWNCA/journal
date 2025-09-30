#!/bin/bash
# Installation script for Coding Journal Manager

echo "🔧 Installing Coding Journal Manager..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Make script executable
chmod +x journal_manager.py

# Create symlink for easy access
if [ -w /usr/local/bin ]; then
    ln -sf "$(pwd)/journal_manager.py" /usr/local/bin/journal-manager
    echo "✅ Installed globally as 'journal-manager'"
else
    echo "💡 To use globally, run: sudo ln -sf $(pwd)/journal_manager.py /usr/local/bin/journal-manager"
fi

echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  python3 journal_manager.py"
echo "  # or if symlinked:"
echo "  journal-manager"
echo ""
echo "First run will guide you through configuration."