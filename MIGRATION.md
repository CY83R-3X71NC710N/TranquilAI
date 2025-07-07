# Migration Guide

## ✅ New Consolidated Script

The new `wallpaper_generator.py` replaces all the old scripts with a single, more powerful Python file.

## 📁 Old Files (Can be removed)

The following files are now **obsolete** and can be safely deleted:

1. **`generate_wallpaper.py`** - Replaced by `wallpaper_generator.py`
2. **`macos-gen-ai-wallpaper.sh`** - Functionality merged into `wallpaper_generator.py`
3. **`setup.sh`** - Setup is now handled by `wallpaper_generator.py --setup`

## 🔄 How to Migrate

### Step 1: Install prerequisites
```bash
# Install requests library
pip install requests --user
```

### Step 2: Run the new setup
```bash
python3 wallpaper_generator.py --setup
```

### Step 2: Test the new script
```bash
python3 wallpaper_generator.py "test prompt" --generate-only
```

### Step 3: Remove old files (optional)
```bash
rm generate_wallpaper.py
rm macos-gen-ai-wallpaper.sh  
rm setup.sh
```

## 📋 Command Comparison

### Old Way
```bash
# Setup
./setup.sh

# Generate wallpaper
./macos-gen-ai-wallpaper.sh "mountain landscape" ~/Pictures/Wallpapers
```

### New Way
```bash
# Setup (one time)
pip install requests --user
python3 wallpaper_generator.py --setup

# Generate wallpaper
python3 wallpaper_generator.py "mountain landscape" --save-dir ~/Pictures/Wallpapers
```

## ✨ New Features

The consolidated script adds several improvements:

1. **Better error handling** - More robust wallpaper setting
2. **Multiple tools support** - wallpaper-cli, m-cli, or AppleScript
3. **Flexible resolution** - Any resolution, not just fixed sizes
4. **Generate-only mode** - Create images without setting them
5. **Improved CLI** - Better argument parsing and help
6. **Auto-setup** - Dependencies installed automatically
7. **Cross-platform preparation** - Code structured for future Linux/Windows support

## 🔧 Troubleshooting Migration

If you have issues:

1. Make sure Python 3.6+ is installed
2. Run the setup command first
3. Check that the script is executable: `chmod +x wallpaper_generator.py`
4. Try the AppleScript fallback: `--tool applescript`
