#!/bin/zsh

source ~/.zshrc

# Check if prompt is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 \"<PROMPT>\" [SAVE_DIRECTORY]"
    exit 1
fi

# Assign command line arguments to variables
PROMPT="$1"

# Optional directory to save all generated images
if [ $# -ge 2 ]; then
    SAVE_DIR="$2"
    mkdir -p "$SAVE_DIR"
else
    SAVE_DIR=""
fi

# Internal directory used by the script to queue images for the next run
QUEUED_DIR="./queued-images"
# Force a refresh of the desktop
killall Dock

# Ensure the queued images directory exists
mkdir -p "$QUEUED_DIR"

# Detect the number of connected displays
NUM_DISPLAYS=$(system_profiler SPDisplaysDataType | grep -c "Resolution:")
if [ "$NUM_DISPLAYS" -eq 0 ]; then
    NUM_DISPLAYS=1
fi

echo "Number of displays detected: $NUM_DISPLAYS"
# # Force a refresh of the desktop
# killall Dock

# Ensure 'wallpaper-cli' is installed
if ! command -v wallpaper &>/dev/null; then
    echo "'wallpaper-cli' is not installed. Please install it using:"
    echo "npm install --global wallpaper-cli"
    exit 1
fi

# Ensure Python3 is installed
if ! command -v python3 &>/dev/null; then
    echo "'python3' is not installed. Please install Python 3."
    exit 1
fi

# Check if requests module is available
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Python 'requests' module is not installed. Installing it now..."
    python3 -m pip install requests
    if [ $? -ne 0 ]; then
        echo "Failed to install requests module. Please install it manually:"
        echo "pip3 install requests"
        exit 1
    fi
fi

# Check if pollinations package is available (optional)
python3 -c "import pollinations" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Optional: Installing pollinations package for enhanced features..."
    python3 -m pip install pollinations 2>/dev/null || echo "Note: pollinations package installation failed, will use direct API method"
fi

# Set wallpapers from previous images in the queued directory
echo "Setting wallpapers from $QUEUED_DIR"
for ((index = 1; index <= NUM_DISPLAYS; index++)); do
    # Add a delay before setting each wallpaper
    sleep 1
    # Note: wallpaper-cli uses zero-based indexing
    SCREEN_INDEX=$((index - 1))
    IMAGE_FILE="$QUEUED_DIR/wallpaper_display_${index}.png"

    if [ -f "$IMAGE_FILE" ]; then
        # Print the command that sets the wallpaper
        echo "Running command: wallpaper \"$IMAGE_FILE\" --screen=$SCREEN_INDEX"

        # Set the wallpaper and capture any output or errors
        WALLPAPER_OUTPUT=$(wallpaper "$IMAGE_FILE" --screen=$SCREEN_INDEX 2>&1)

        if [ $? -eq 0 ]; then
            echo "Wallpaper set successfully for display $index"
        else
            echo "Failed to set wallpaper for display $index"
            echo "Error: $WALLPAPER_OUTPUT"
        fi
    else
        echo "No queued wallpaper found for display $index"
    fi
done

# Force a refresh of the desktop
killall Dock
# Now proceed to generate new images using Python
echo "Generating new wallpapers using Python with highest quality settings..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/generate_wallpaper.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python wallpaper generator script not found at $PYTHON_SCRIPT"
    exit 1
fi

# Loop over each display and generate high-quality images using Python
for ((index = 1; index <= NUM_DISPLAYS; index++)); do
    echo "Processing display $index with Python generator"

    QUEUED_IMAGE_FILE="$QUEUED_DIR/wallpaper_display_${index}.png"
    
    echo "Generating ultra-high quality wallpaper (2048x1152) for display $index..."
    
    # Call Python script to generate wallpaper
    if [ -n "$SAVE_DIR" ]; then
        python3 "$PYTHON_SCRIPT" "$PROMPT" "$index" "$QUEUED_IMAGE_FILE" "$SAVE_DIR"
    else
        python3 "$PYTHON_SCRIPT" "$PROMPT" "$index" "$QUEUED_IMAGE_FILE"
    fi
    
    # Check if Python script succeeded
    if [ $? -eq 0 ] && [ -f "$QUEUED_IMAGE_FILE" ] && [ -s "$QUEUED_IMAGE_FILE" ]; then
        echo "High-quality wallpaper generated successfully for display $index"
        echo "Saved to queued images: $QUEUED_IMAGE_FILE"
        
        # Get file size for verification
        FILE_SIZE=$(du -h "$QUEUED_IMAGE_FILE" | cut -f1)
        echo "File size: $FILE_SIZE"
    else
        echo "Failed to generate wallpaper for display $index"
        continue
    fi
done

echo "Wallpaper generation process completed."
