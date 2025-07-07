#!/bin/bash
# Quick setup script for macOS AI Wallpaper Generator

echo "🎨 Setting up macOS AI Wallpaper Generator"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS"
    exit 1
fi

# Install requests library
echo "📦 Installing requests library..."
python3 -m pip install requests --user

# Check if Homebrew is installed (for wallpaper tools)
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew (for wallpaper tools)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew is already installed"
fi

# Run the Python setup
echo "🐍 Setting up wallpaper tools..."
python3 wallpaper_generator.py --setup

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 Try it out:"
echo "   python3 wallpaper_generator.py \"serene mountain landscape\" --generate-only"
echo "   ./generate-wallpaper \"cyberpunk cityscape\""
