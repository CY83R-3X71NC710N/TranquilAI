# macOS AI Wallpaper Generator

A consolidated Python script that generates AI wallpapers using the Pollinations API and sets them as desktop backgrounds on macOS.

## Features

- **Single Script**: All functionality consolidated into one Python file
- **Pollinations Only**: Uses only the `pollinations` library for AI image generation
- **Multiple Wallpaper Tools**: Supports wallpaper-cli, m-cli, and AppleScript for setting wallpapers
- **Multi-Display Support**: Automatically detects and generates wallpapers for multiple displays
- **High Quality**: Uses the Flux model for best image quality
- **Backup & Queue**: Saves copies and queues images for rotation

## Quick Start

### 1. Setup (One-time)
```bash
python3 wallpaper_generator.py --setup
```

This will automatically:
- Install the `pollinations` Python package
- Install a wallpaper setting tool (wallpaper-cli or m-cli via Homebrew)
- Set up all dependencies

### 2. Generate and Set Wallpapers
```bash
# Using the Python script directly
python3 wallpaper_generator.py "a serene mountain landscape at sunset"

# Or using the convenient wrapper
./generate-wallpaper "a serene mountain landscape at sunset"
```

### 3. Advanced Usage

#### Custom Resolution
```bash
./generate-wallpaper "cyberpunk city neon lights" --resolution 2560x1440
```

#### Save Copies
```bash
./generate-wallpaper "abstract art colorful" --save-dir ~/Pictures/AI-Wallpapers
```

#### Generate Only (Don't Set)
```bash
./generate-wallpaper "ocean waves" --generate-only
```

#### Specific Wallpaper Tool
```bash
./generate-wallpaper "forest path" --tool applescript
```

## Wallpaper Setting Methods

The script tries multiple methods to set wallpapers (in order of preference):

1. **wallpaper-cli** - Cross-platform Node.js tool
2. **m-cli** - macOS-specific Homebrew tool  
3. **AppleScript** - Built-in macOS scripting (fallback)

## Command Line Options

```
positional arguments:
  prompt                Text prompt for image generation

options:
  -h, --help            show this help message and exit
  --displays DISPLAYS   Number of displays (auto-detect if not specified)
  --save-dir SAVE_DIR   Directory to save copies of generated images
  --resolution RESOLUTION
                        Image resolution (e.g., 1920x1080, 2560x1440)
  --tool {wallpaper-cli,m-cli,applescript,auto}
                        Wallpaper setting tool to use
  --queue-dir QUEUE_DIR
                        Directory for queued wallpaper images
  --setup               Install required dependencies
  --generate-only       Only generate images, don't set as wallpaper
```

## How It Works

1. **Display Detection**: Automatically detects the number of connected displays
2. **Image Generation**: Uses Pollinations API with Flux model for high-quality images
3. **Queue System**: Saves images to a queue directory for rotation
4. **Wallpaper Setting**: Uses the best available tool to set wallpapers per display
5. **Desktop Refresh**: Refreshes the desktop to apply changes

## Requirements

- macOS (tested on macOS 10.15+)
- Python 3.6+
- Internet connection for image generation

## Dependencies (Auto-installed)

- `pollinations` - AI image generation
- `wallpaper-cli` or `m-cli` - Wallpaper setting (installed via setup)

## Examples

### Nature Scene
```bash
./generate-wallpaper "peaceful forest with morning mist and sunbeams"
```

### Abstract Art
```bash
./generate-wallpaper "geometric abstract art with vibrant colors"
```

### Cityscape
```bash
./generate-wallpaper "futuristic city skyline at night with neon lights"
```

### Space Theme
```bash
./generate-wallpaper "deep space nebula with stars and galaxies"
```

## Troubleshooting

### Permission Issues
If you get permission errors, make sure the script is executable:
```bash
chmod +x wallpaper_generator.py
```

### Wallpaper Not Setting
Try using AppleScript method specifically:
```bash
python3 wallpaper_generator.py "your prompt" --tool applescript
```

### Network Issues
The script requires internet access for the Pollinations API. Check your connection.

### Multiple Displays
The script automatically detects displays. If detection fails, specify manually:
```bash
python3 wallpaper_generator.py "your prompt" --displays 2
```

## Migration from Old Scripts

This single script replaces:
- `generate_wallpaper.py`
- `macos-gen-ai-wallpaper.sh` 
- `setup.sh`

See `MIGRATION.md` for detailed migration instructions.

### Quick Migration
1. Run setup: `python3 wallpaper_generator.py --setup`
2. Test: `./generate-wallpaper "test prompt" --generate-only`
3. Remove old files: `rm generate_wallpaper.py macos-gen-ai-wallpaper.sh setup.sh`
