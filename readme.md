UPDATE: I have made this project into a proper app: https://www.aiwallpapergenerator.ai/

Get [Shortery](https://apps.apple.com/us/app/shortery/id1594183810?mt=12) (it's free) and set it to run the shortcut on login

Now, the script will run automatically each time you log in, setting a new AI-generated wallpaper straight away (from the queue) and generating new ultra-high quality images for the next run

## Project Structure

- `macos-gen-ai-wallpaper.sh` - Main shell script that orchestrates the wallpaper setting and generation
- `generate_wallpaper.py` - Python script for high-quality image generation using Pollinations AI
- `setup.sh` - Installation script for all dependencies
- `queued-images/` - Directory containing wallpapers ready to be set (created automatically)

## Troubleshooting

### Python Dependencies
If you encounter issues with Python packages:
```bash
# Install requests manually
pip3 install requests

# Install pollinations package (optional)
pip3 install pollinations
```

### Permission Issues
Make sure scripts are executable:
```bash
chmod +x macos-gen-ai-wallpaper.sh
chmod +x generate_wallpaper.py
chmod +x setup.sh
```acOS AI Wallpaper Generator

This script generates ultra-high quality AI wallpapers for your macOS system using Pollinations AI with Python (completely free, no API key required!). It automatically sets the generated images as your desktop background on login, and generates some for the next time (works for multiple displays)

## Prerequisites

- macOS operating system
- Node.js and npm (for wallpaper-cli)
- Python 3.x
- Homebrew package manager (for installing dependencies)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/macos-gen-ai-wallpaper.git
   cd macos-gen-ai-wallpaper
   ```

2. Run the setup script to install dependencies:

   ```
   ./setup.sh
   ```

   This script will install the required dependencies, including the `wallpaper-cli` tool, Python 3, and required Python packages (`requests` and optionally `pollinations`).

### First Run

Run the script manually the first time to generate the initial set of wallpapers:

```
./macos-gen-ai-wallpaper.sh "a breathtaking view of an interesting part or thing in the world that will really just wow me emotionally. Be creative and make it look realistic. it can be literally anything surprise me. i like technology so maybe incorporate that in too." [optional-save-directory]
```

Note: No API key required! Pollinations AI is completely free to use.

This will create a queue of ultra-high quality images (2048x1152 resolution) for the next run.

### Automatic Run on Login

Create a macOS shortcut (in shortcuts.app) that runs this script.

```bash

PATH=<whatever your path is when you echo $PATH>

cd <path to project>/macos-gen-ai-wallpaper-on-login

./macos-gen-ai-wallpaper.sh "<Your prompt here>" [optional-save-directory]
```

## Features

- **Free and No API Key Required**: Uses Pollinations AI which is completely free
- **Ultra-High Quality Images**: Generates 2048x1152 resolution wallpapers using the Flux model
- **No Watermarks**: Configured to generate images without Pollinations watermarks
- **Multi-Display Support**: Automatically detects and generates unique wallpapers for each connected display
- **Automatic Wallpaper Setting**: Sets wallpapers immediately from previous generation queue
- **Background Generation**: Generates new wallpapers for the next run while you use your computer
- **Python-Powered**: Uses official Pollinations methods with fallback to direct API calls
- **Enhanced Quality**: Flux model provides superior image quality and detail

## Technical Details

### Image Generation
- **Resolution**: 2048x1152 (16:9 ultra-high definition)
- **Model**: Flux (highest quality model available)
- **Format**: PNG for lossless quality
- **Unique Seeds**: Each display gets a different image using timestamp-based seeds

### Python Implementation
The script uses a dedicated Python module (`generate_wallpaper.py`) that:
1. First attempts to use the official `pollinations` package if available
2. Falls back to direct API calls for maximum compatibility
3. Implements proper error handling and retry logic
4. Supports both methods shown in the Pollinations documentation

## How Pollinations AI Works

Pollinations AI is a free, open-source AI image generation service that doesn't require API keys or registration. The script uses optimized parameters to:
- Generate ultra-high-resolution 2048x1152 images
- Use the Flux model for maximum quality and detail
- Remove watermarks with the `nologo=true` parameter
- Enable image enhancement for better quality
- Use unique seeds for each display to ensure different images

Get [Shortery](https://apps.apple.com/us/app/shortery/id1594183810?mt=12) (it's free) and set it to run the shortcut on login

Now, the script will run automatically each time you log in, setting a new AI-generated wallpaper straight away (from the queue) and generating new images for the next run
