#!/usr/bin/env python3
"""
Consolidated macOS AI Wallpaper Generator
Uses only pollinations library for image generation and provides multiple options for setting wallpapers
"""

import sys
import os
import time
import subprocess
import shutil
import argparse
from pathlib import Path

try:
    import pollinations
except ImportError:
    print("Installing pollinations package...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pollinations"])
    import pollinations

def ensure_homebrew():
    """Ensure Homebrew is installed on macOS"""
    try:
        subprocess.run(["brew", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Homebrew not found. Installing Homebrew...")
        try:
            subprocess.run([
                "/bin/bash", "-c", 
                "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            ], check=True)
            return True
        except subprocess.CalledProcessError:
            print("Failed to install Homebrew")
            return False

def install_wallpaper_tool():
    """Install a wallpaper setting tool"""
    # Try different wallpaper tools in order of preference
    tools = [
        {"name": "wallpaper-cli", "install_cmd": ["npm", "install", "-g", "wallpaper-cli"], "test_cmd": ["wallpaper", "--help"]},
        {"name": "m-cli", "install_cmd": ["brew", "install", "m-cli"], "test_cmd": ["m", "wallpaper", "help"]},
    ]
    
    for tool in tools:
        try:
            # Test if already installed
            subprocess.run(tool["test_cmd"], check=True, capture_output=True)
            print(f"✓ {tool['name']} is already installed")
            return tool["name"]
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    # Try to install tools
    for tool in tools:
        try:
            print(f"Installing {tool['name']}...")
            subprocess.run(tool["install_cmd"], check=True)
            subprocess.run(tool["test_cmd"], check=True, capture_output=True)
            print(f"✓ {tool['name']} installed successfully")
            return tool["name"]
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to install {tool['name']}: {e}")
            continue
    
    return None

def set_wallpaper_applescript(image_path, display_index=None):
    """Set wallpaper using AppleScript (built-in macOS method)"""
    try:
        if display_index is not None:
            # For specific display
            script = f'''
            tell application "System Events"
                tell desktop {display_index}
                    set picture to "{image_path}"
                end tell
            end tell
            '''
        else:
            # For all displays
            script = f'''
            tell application "System Events"
                tell every desktop
                    set picture to "{image_path}"
                end tell
            end tell
            '''
        
        result = subprocess.run(["osascript", "-e", script], 
                              capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"AppleScript error: {e.stderr}")
        return False

def set_wallpaper_wallpaper_cli(image_path, display_index=None):
    """Set wallpaper using wallpaper-cli"""
    try:
        if display_index is not None:
            # wallpaper-cli uses 0-based indexing
            screen_index = display_index - 1
            cmd = ["wallpaper", image_path, f"--screen={screen_index}"]
        else:
            cmd = ["wallpaper", image_path]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"wallpaper-cli error: {e}")
        return False

def set_wallpaper_m_cli(image_path, display_index=None):
    """Set wallpaper using m-cli"""
    try:
        if display_index is not None:
            cmd = ["m", "wallpaper", image_path, "--display", str(display_index)]
        else:
            cmd = ["m", "wallpaper", image_path]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"m-cli error: {e}")
        return False

def get_display_count():
    """Get number of connected displays using system_profiler"""
    try:
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType"],
            capture_output=True, text=True, check=True
        )
        count = result.stdout.count("Resolution:")
        return max(1, count)  # Ensure at least 1 display
    except subprocess.CalledProcessError:
        return 1  # Default to 1 display if detection fails

def generate_wallpaper_with_pollinations(prompt, width, height, seed, output_file):
    """Generate wallpaper using the pollinations package"""
    try:
        print(f"Generating image with pollinations...")
        print(f"  Model: flux")
        print(f"  Resolution: {width}x{height}")
        print(f"  Seed: {seed}")
        print(f"  Prompt: {prompt}")
        
        # Create model with flux for highest quality
        model = pollinations.Image(
            model="flux",
            width=width,
            height=height,
            seed=seed
        )
        
        # Generate and save image
        model.Generate(
            prompt=prompt,
            save=True
        )
        
        # The package typically saves with various default names, check common patterns
        possible_files = [
            "generated_image.png",
            "image.png", 
            f"{seed}.png",
            "output.png",
            "flux_generated.png",
            "pollinations_output.png"
        ]
        
        # Check for the generated file
        for possible_file in possible_files:
            if os.path.exists(possible_file):
                if possible_file != output_file:
                    shutil.move(possible_file, output_file)
                print(f"✓ Image generated successfully: {output_file}")
                return True
        
        # If no standard file found, check current directory for any new PNG files
        png_files = [f for f in os.listdir('.') if f.endswith('.png') and os.path.isfile(f)]
        if png_files:
            # Use the most recently created PNG file
            latest_file = max(png_files, key=os.path.getctime)
            if latest_file != output_file:
                shutil.move(latest_file, output_file)
            print(f"✓ Image generated successfully: {output_file}")
            return True
        
        print("✗ Failed to locate generated image file")
        return False
        
    except Exception as e:
        print(f"✗ Error generating image with pollinations: {str(e)}")
        return False

def set_wallpaper(image_path, display_index=None, tool=None):
    """Set wallpaper using the best available method"""
    abs_image_path = os.path.abspath(image_path)
    
    if not os.path.exists(abs_image_path):
        print(f"✗ Image file not found: {abs_image_path}")
        return False
    
    # Try different methods in order of preference
    methods = []
    
    if tool == "wallpaper-cli":
        methods = [("wallpaper-cli", set_wallpaper_wallpaper_cli)]
    elif tool == "m-cli":
        methods = [("m-cli", set_wallpaper_m_cli)]
    elif tool == "applescript":
        methods = [("AppleScript", set_wallpaper_applescript)]
    else:
        # Auto-detect best method
        methods = [
            ("wallpaper-cli", set_wallpaper_wallpaper_cli),
            ("m-cli", set_wallpaper_m_cli),
            ("AppleScript", set_wallpaper_applescript)
        ]
    
    for method_name, method_func in methods:
        try:
            print(f"Setting wallpaper using {method_name}...")
            if method_func(abs_image_path, display_index):
                print(f"✓ Wallpaper set successfully using {method_name}")
                return True
        except Exception as e:
            print(f"✗ {method_name} failed: {e}")
            continue
    
    print("✗ All wallpaper setting methods failed")
    return False

def refresh_desktop():
    """Refresh desktop to apply wallpaper changes"""
    try:
        subprocess.run(["killall", "Dock"], check=True)
        print("✓ Desktop refreshed")
    except subprocess.CalledProcessError:
        print("⚠ Could not refresh desktop")

def main():
    parser = argparse.ArgumentParser(description="macOS AI Wallpaper Generator")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--displays", type=int, default=None, 
                       help="Number of displays (auto-detect if not specified)")
    parser.add_argument("--save-dir", help="Directory to save copies of generated images")
    parser.add_argument("--resolution", default="1920x1080", 
                       help="Image resolution (e.g., 1920x1080, 2560x1440)")
    parser.add_argument("--tool", choices=["wallpaper-cli", "m-cli", "applescript", "auto"],
                       default="auto", help="Wallpaper setting tool to use")
    parser.add_argument("--queue-dir", default="./queued-images",
                       help="Directory for queued wallpaper images")
    parser.add_argument("--setup", action="store_true",
                       help="Install required dependencies")
    parser.add_argument("--generate-only", action="store_true",
                       help="Only generate images, don't set as wallpaper")
    
    args = parser.parse_args()
    
    # Setup mode
    if args.setup:
        print("Setting up macOS AI Wallpaper Generator...")
        
        # Check if we're on macOS
        if sys.platform != "darwin":
            print("✗ This script is designed for macOS")
            sys.exit(1)
        
        # Install wallpaper tool
        tool = install_wallpaper_tool()
        if tool:
            print(f"✓ Wallpaper tool '{tool}' is ready")
        else:
            print("⚠ No wallpaper tool installed, will use AppleScript as fallback")
        
        print("✓ Setup complete!")
        return
    
    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
    except ValueError:
        print("✗ Invalid resolution format. Use WIDTHxHEIGHT (e.g., 1920x1080)")
        sys.exit(1)
    
    # Detect displays
    if args.displays:
        num_displays = args.displays
    else:
        num_displays = get_display_count()
    
    print(f"Target displays: {num_displays}")
    
    # Create directories
    queue_dir = Path(args.queue_dir)
    queue_dir.mkdir(exist_ok=True)
    
    if args.save_dir:
        save_dir = Path(args.save_dir)
        save_dir.mkdir(exist_ok=True)
    
    # Set existing wallpapers from queue (if not generate-only mode)
    if not args.generate_only:
        print("\n=== Setting Queued Wallpapers ===")
        for display_idx in range(1, num_displays + 1):
            queued_file = queue_dir / f"wallpaper_display_{display_idx}.png"
            if queued_file.exists():
                set_wallpaper(str(queued_file), display_idx, args.tool)
            else:
                print(f"No queued wallpaper for display {display_idx}")
        
        refresh_desktop()
    
    # Generate new wallpapers
    print(f"\n=== Generating New Wallpapers ===")
    success_count = 0
    
    for display_idx in range(1, num_displays + 1):
        print(f"\n--- Display {display_idx} ---")
        
        # Use current timestamp + display index as seed for uniqueness
        seed = int(time.time()) + display_idx
        
        # Output file
        output_file = queue_dir / f"wallpaper_display_{display_idx}.png"
        
        # Generate wallpaper
        if generate_wallpaper_with_pollinations(args.prompt, width, height, seed, str(output_file)):
            success_count += 1
            
            # Save copy if requested
            if args.save_dir:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_filename = f"wallpaper_display_{display_idx}_{timestamp}.png"
                save_path = save_dir / save_filename
                try:
                    shutil.copy2(str(output_file), str(save_path))
                    print(f"✓ Saved copy to: {save_path}")
                except Exception as e:
                    print(f"⚠ Failed to save copy: {e}")
        else:
            print(f"✗ Failed to generate wallpaper for display {display_idx}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully generated {success_count}/{num_displays} wallpapers")
    
    if success_count > 0:
        print("✓ Wallpaper generation completed successfully")
        if args.generate_only:
            print("Images saved to queue directory for future use")
        else:
            print("Run the script again to set the new wallpapers")
    else:
        print("✗ No wallpapers were generated successfully")
        sys.exit(1)

if __name__ == "__main__":
    main()
