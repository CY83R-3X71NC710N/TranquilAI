#!/bin/bash

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed."

    # Detect the operating system
    OS=$(uname -s)
    case "$OS" in
        Darwin)
            echo "Detected macOS."
            echo "Attempting to install Node.js and npm using Homebrew."

            # Check if Homebrew is installed
            if ! command -v brew &> /dev/null; then
                echo "Homebrew is not installed. Installing Homebrew first."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

                # Add Homebrew to PATH
                echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.bash_profile
                eval "$(/opt/homebrew/bin/brew shellenv)"
            fi

            # Install Node.js (which includes npm)
            brew install node

            ;;
        Linux)
            echo "Detected Linux."

            # Check for common package managers and install Node.js
            if command -v apt-get &> /dev/null; then
                echo "Using apt-get to install Node.js and npm."
                sudo apt-get update
                sudo apt-get install -y nodejs npm
            elif command -v yum &> /dev/null; then
                echo "Using yum to install Node.js and npm."
                sudo yum install -y nodejs npm
            elif command -v pacman &> /dev/null; then
                echo "Using pacman to install Node.js and npm."
                sudo pacman -Sy nodejs npm
            else
                echo "Could not detect a supported package manager."
                echo "Please install Node.js and npm manually."
                exit 1
            fi

            ;;
        *)
            echo "Unsupported operating system."
            echo "Please install npm manually."
            exit 1
            ;;
    esac

else
    echo "npm is installed."
fi

# Install wallpaper-cli globally
echo "Installing wallpaper-cli globally."
npm install --global wallpaper-cli

if [ $? -eq 0 ]; then
    echo "wallpaper-cli installed successfully."
else
    echo "Failed to install wallpaper-cli."
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed."
    
    # Detect the operating system and install Python3
    OS=$(uname -s)
    case "$OS" in
        Darwin)
            echo "Installing Python3 on macOS using Homebrew."
            if command -v brew &> /dev/null; then
                brew install python
            else
                echo "Homebrew not found. Please install Python3 manually:"
                echo "Visit: https://www.python.org/downloads/"
                exit 1
            fi
            ;;
        Linux)
            echo "Installing Python3 on Linux."
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3 python3-pip
            elif command -v pacman &> /dev/null; then
                sudo pacman -Sy python python-pip
            else
                echo "Could not detect a supported package manager for Python3 installation."
                echo "Please install Python3 manually."
                exit 1
            fi
            ;;
        *)
            echo "Unsupported operating system for automatic Python3 installation."
            echo "Please install Python3 manually: https://www.python.org/downloads/"
            exit 1
            ;;
    esac
else
    echo "Python3 is already installed."
fi

# Install required Python packages
echo "Installing required Python packages..."

# Install requests (required)
python3 -m pip install requests
if [ $? -eq 0 ]; then
    echo "Python requests package installed successfully."
else
    echo "Failed to install Python requests package."
    exit 1
fi

# Install pollinations package (optional, enhanced features)
echo "Installing pollinations package for enhanced features..."
python3 -m pip install pollinations
if [ $? -eq 0 ]; then
    echo "Pollinations package installed successfully."
else
    echo "Note: Failed to install pollinations package, but this is optional."
    echo "The script will use direct API calls instead."
fi
