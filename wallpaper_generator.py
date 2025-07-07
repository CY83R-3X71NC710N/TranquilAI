#!/usr/bin/env python3
"""
macOS AI Wallpaper Generator
Uses Google Gemini 2.5 Pro for prompt enhancement and Pollinations for image generation
"""

import sys
import os
import time
import subprocess
import shutil
import argparse
import tempfile
import urllib.parse
import random
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests package...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--user"])
    import requests

# Try to import Google Gemini dependencies for prompt enhancement
try:
    from google import genai
    from dotenv import load_dotenv
    GEMINI_AVAILABLE = True
    # Load environment variables
    load_dotenv()
except ImportError:
    GEMINI_AVAILABLE = False

# Try to import image processing dependencies
try:
    from PIL import Image, ImageEnhance, ImageFilter
    import numpy as np
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False

def run_command(cmd, capture_output=True, shell=False):
    """Run a command and return the result."""
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        else:
            result = subprocess.run(cmd, capture_output=capture_output, text=True)
        return result
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def download_image_from_pollinations(prompt, width, height, seed, model, output_file, private=False):
    """Download image from Pollinations API"""
    try:
        # URL encode the prompt to handle special characters
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Construct the Pollinations API URL with maximum quality settings
        if private:
            # Private mode - minimal parameters for privacy but still high quality
            image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&model={model}&nologo=true&private=true"
        else:
            # Standard mode - with nologo, enhance, and maximum quality parameters
            image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&model={model}&nologo=true&enhance=true&private=true&quality=high&steps=120"
        
        print(f"Downloading image from Pollinations API...")
        print(f"  URL: {image_url}")
        
        # Download the image
        response = requests.get(image_url, timeout=60)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Write the content to the output file
        with open(output_file, 'wb') as file:
            file.write(response.content)
        
        # Verify the file was created and has content
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"✓ Image downloaded successfully: {output_file}")
            return True
        else:
            print("✗ Image download failed - file not created or empty")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error downloading image: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error downloading image: {str(e)}")
        return False

def enhance_prompt_with_gemini(user_prompt):
    """Enhance user prompt using Gemini 2.5 Pro for better AI wallpaper generation"""
    try:
        if not GEMINI_AVAILABLE:
            print("  Gemini not available, using original prompt")
            return add_no_text_instruction(user_prompt)
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("  No Gemini API key found, using original prompt")
            return add_no_text_instruction(user_prompt)
        
        print("  Enhancing prompt with Gemini 2.5 Pro...")
        
        # Configure Gemini
        client = genai.Client(api_key=api_key)
        
        # Create enhancement prompt
        enhancement_prompt = f"""You are an expert AI art prompt engineer. Your task is to enhance the following user prompt to create stunning, high-quality wallpapers.

Transform this prompt into a detailed, vivid description that will generate beautiful wallpaper images. Focus on:
- Visual details (lighting, colors, atmosphere, composition)
- Artistic style and quality descriptors
- Wallpaper-appropriate elements (suitable for desktop backgrounds)
- Professional photography/art terminology
- IMPORTANT: The image must contain NO TEXT, NO LETTERS, NO WORDS, NO CAPTIONS

Keep the core concept but make it much more descriptive and visually rich. Keep response under 200 words.

Original prompt: "{user_prompt}"

Enhanced prompt:"""

        # Generate enhanced prompt
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=enhancement_prompt
        )
        
        enhanced_prompt = response.text.strip()
        # Ensure no text instruction is included
        enhanced_prompt = add_no_text_instruction(enhanced_prompt)
        print(f"  ✓ Enhanced: {enhanced_prompt[:100]}...")
        return enhanced_prompt
        
    except Exception as e:
        print(f"  ⚠ Gemini enhancement failed: {str(e)}")
        print("  Using original prompt")
        return add_no_text_instruction(user_prompt)

def generate_wallpaper(prompt, width, height, seed, output_file, private=False, no_enhance=False):
    """Generate wallpaper using Gemini-enhanced prompts and Pollinations API"""
    try:
        print(f"Generating wallpaper...")
        print(f"  Model: Pollinations AI (Flux)")
        print(f"  Resolution: {width}x{height}")
        print(f"  Seed: {seed}")
        print(f"  Private mode: {'Yes' if private else 'No'}")
        print(f"  Original prompt: {prompt}")
        
        # Enhance prompt with Gemini if available and not in private mode
        if not private:
            enhanced_prompt = enhance_prompt_with_gemini(prompt)
        else:
            print("  Private mode: skipping prompt enhancement")
            enhanced_prompt = add_no_text_instruction(prompt)
        
        print(f"  Final prompt: {enhanced_prompt}")
        
        # Download the image first
        download_success = download_image_from_pollinations(enhanced_prompt, width, height, seed, "flux", output_file, private)
        
        if download_success and not no_enhance:
            # Apply post-processing effects to enhance image quality
            enhanced_output = enhance_image_quality(output_file)
            return enhanced_output == output_file  # Return True if processing succeeded
        elif download_success and no_enhance:
            print("  Post-processing disabled by user")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error generating wallpaper: {str(e)}")
        return False

def install_wallpaper_tool():
    """Install a wallpaper setting tool"""
    print("Installing wallpaper setting tool...")
    
    # Try wallpaper-cli first
    result = run_command(["npm", "install", "-g", "wallpaper-cli"])
    if result and result.returncode == 0:
        print("✓ wallpaper-cli installed successfully")
        return "wallpaper-cli"
    
    # Try m-cli as alternative
    result = run_command(["brew", "install", "m-cli"])
    if result and result.returncode == 0:
        print("✓ m-cli installed successfully")
        return "m-cli"
    
    print("Using AppleScript as fallback")
    return "applescript"

def check_wallpaper_tool(tool):
    """Check if a wallpaper tool is available."""
    if tool == "wallpaper-cli":
        result = run_command(["which", "wallpaper"])
        return result and result.returncode == 0
    elif tool == "m-cli":
        result = run_command(["which", "m"])
        return result and result.returncode == 0
    elif tool == "applescript":
        return True  # AppleScript is always available on macOS
    return False

def get_display_count():
    """Get number of connected displays using AppleScript"""
    try:
        result = run_command([
            "osascript", "-e",
            'tell application "System Events" to count (every desktop)'
        ])
        if result and result.returncode == 0:
            return int(result.stdout.strip())
    except:
        pass
    return 1  # Default to 1 display if detection fails

def get_display_resolution():
    """Get the primary display resolution."""
    try:
        result = run_command([
            "osascript", "-e",
            'tell application "Finder" to get bounds of window of desktop'
        ])
        if result and result.returncode == 0:
            # Parse output like "0, 0, 1920, 1080"
            bounds = result.stdout.strip().split(", ")
            if len(bounds) >= 4:
                width = int(bounds[2])
                height = int(bounds[3])
                return width, height
    except:
        pass
    return 5120, 2880  # Default to 5K resolution for maximum quality on macOS

def set_wallpaper(image_path, display_index=None, tool=None):
    """Set wallpaper using the best available method"""
    abs_image_path = os.path.abspath(image_path)
    
    if not os.path.exists(abs_image_path):
        print(f"✗ Image file not found: {abs_image_path}")
        return False
    
    print(f"Setting wallpaper using {tool or 'auto-detect'}: {abs_image_path}")
    
    # Try different methods in order of preference
    methods = []
    
    if tool == "wallpaper-cli":
        methods = [("wallpaper-cli", lambda p, d: set_wallpaper_wallpaper_cli(p, d))]
    elif tool == "m-cli":
        methods = [("m-cli", lambda p, d: set_wallpaper_m_cli(p, d))]
    elif tool == "applescript":
        methods = [("AppleScript", lambda p, d: set_wallpaper_applescript(p, d))]
    else:
        # Auto-detect best method
        methods = [
            ("wallpaper-cli", lambda p, d: set_wallpaper_wallpaper_cli(p, d)),
            ("m-cli", lambda p, d: set_wallpaper_m_cli(p, d)),
            ("AppleScript", lambda p, d: set_wallpaper_applescript(p, d))
        ]
    
    for method_name, method_func in methods:
        if check_wallpaper_tool(method_name):
            try:
                if method_func(abs_image_path, display_index):
                    print(f"✓ Wallpaper set successfully using {method_name}")
                    return True
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
                continue
    
    print("✗ All wallpaper setting methods failed")
    return False

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
            tell application "Finder"
                set desktop picture to POSIX file "{image_path}"
            end tell
            '''
        
        result = run_command(["osascript", "-e", script])
        return result and result.returncode == 0
    except Exception as e:
        print(f"AppleScript error: {e}")
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
        
        result = run_command(cmd)
        return result and result.returncode == 0
    except Exception as e:
        print(f"wallpaper-cli error: {e}")
        return False

def set_wallpaper_m_cli(image_path, display_index=None):
    """Set wallpaper using m-cli"""
    try:
        if display_index is not None:
            cmd = ["m", "wallpaper", image_path, "--display", str(display_index)]
        else:
            cmd = ["m", "wallpaper", image_path]
        
        result = run_command(cmd)
        return result and result.returncode == 0
    except Exception as e:
        print(f"m-cli error: {e}")
        return False

def refresh_desktop():
    """Refresh desktop to apply wallpaper changes"""
    try:
        run_command(["killall", "Dock"])
        time.sleep(1)
        print("✓ Desktop refreshed")
    except:
        print("⚠ Could not refresh desktop")

def setup_dependencies():
    """Set up all required dependencies."""
    print("Setting up dependencies...")
    
    # Check if requests is available
    try:
        import requests
        print("✓ requests library is already available")
    except ImportError:
        print("Installing requests library...")
        result = run_command([sys.executable, "-m", "pip", "install", "requests", "--user"])
        if not result or result.returncode != 0:
            print("Failed to install requests. Please run: pip install requests --user")
            return False
        else:
            print("✓ requests installed successfully")
    
    # Check Gemini dependencies
    try:
        import google.generativeai as genai
        from dotenv import load_dotenv
        print("✓ Gemini dependencies are available")
    except ImportError:
        print("Installing Gemini dependencies...")
        result = run_command([sys.executable, "-m", "pip", "install", "google-generativeai", "python-dotenv", "--user"])
        if not result or result.returncode != 0:
            print("⚠ Failed to install Gemini dependencies. Prompt enhancement will be disabled.")
        else:
            print("✓ Gemini dependencies installed successfully")
    
    # Check image processing dependencies
    try:
        from PIL import Image, ImageEnhance, ImageFilter
        import numpy as np
        print("✓ Image processing dependencies are available")
        # Check for scipy for advanced grain reduction
        try:
            import scipy
            print("✓ Advanced grain reduction (scipy) is available")
        except ImportError:
            print("⚠ scipy not found - advanced grain reduction will use fallback method")
    except ImportError:
        print("Installing image processing dependencies...")
        result = run_command([sys.executable, "-m", "pip", "install", "Pillow", "numpy", "scipy", "--user"])
        if not result or result.returncode != 0:
            print("⚠ Failed to install image processing dependencies. Post-processing will be disabled.")
        else:
            print("✓ Image processing dependencies installed successfully")
    
    # Install wallpaper tool
    tool = install_wallpaper_tool()
    
    print("✓ Setup complete!")
    return True

def enhance_image_quality(image_path, output_path=None):
    """
    Apply subtle, professional post-processing effects to enhance image quality
    Conservative enhancements that preserve natural appearance
    """
    if not IMAGE_PROCESSING_AVAILABLE:
        print("  Image processing libraries not available, skipping enhancement")
        return image_path
    
    try:
        # Use input path as output if not specified
        if output_path is None:
            output_path = image_path
        
        print("  Applying professional image enhancement...")
        print("    • Adaptive brightness correction")
        print("    • Gentle contrast adjustment")
        print("    • Subtle color optimization")
        print("    • Light noise reduction")
        print("    • Careful sharpening")
        
        # Open the image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply gentle enhancements
            enhanced_img = img.copy()
            
            # 1. Adaptive brightness adjustment
            enhanced_img = apply_adaptive_brightness(enhanced_img)
            
            # 2. Gentle contrast enhancement
            contrast_enhancer = ImageEnhance.Contrast(enhanced_img)
            enhanced_img = contrast_enhancer.enhance(1.05)  # Very gentle 5% contrast boost
            
            # 3. Subtle color saturation boost
            color_enhancer = ImageEnhance.Color(enhanced_img)
            enhanced_img = color_enhancer.enhance(1.08)  # Gentle 8% saturation boost
            
            # 4. Light noise reduction
            enhanced_img = apply_gentle_noise_reduction(enhanced_img)
            
            # 5. Subtle sharpening for clarity
            enhanced_img = apply_subtle_sharpening(enhanced_img)
            
            # Save with high quality settings
            enhanced_img.save(output_path, 'JPEG', quality=95, optimize=True, progressive=True)
            
        print("  ✓ Natural enhancement applied successfully")
        return output_path
        
    except Exception as e:
        print(f"  ⚠ Post-processing failed: {str(e)}")
        print("  Using original image")
        return image_path

def apply_adaptive_brightness(img):
    """Apply intelligent brightness adjustment based on image characteristics"""
    try:
        # Analyze image brightness
        img_array = np.array(img)
        mean_brightness = np.mean(img_array)
        
        # Apply conservative brightness adjustments only when needed
        if mean_brightness < 100:  # Very dark image
            brightness_enhancer = ImageEnhance.Brightness(img)
            img = brightness_enhancer.enhance(1.15)  # 15% boost
        elif mean_brightness < 120:  # Somewhat dark
            brightness_enhancer = ImageEnhance.Brightness(img)
            img = brightness_enhancer.enhance(1.08)  # 8% boost
        elif mean_brightness > 220:  # Very bright
            brightness_enhancer = ImageEnhance.Brightness(img)
            img = brightness_enhancer.enhance(0.95)  # 5% reduction
        
        return img
    except Exception:
        return img

def apply_gentle_noise_reduction(img):
    """Apply light noise reduction without losing detail"""
    try:
        # Very gentle blur for noise reduction
        denoised = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        # Convert to arrays
        original_array = np.array(img).astype(np.float32)
        denoised_array = np.array(denoised).astype(np.float32)
        
        # Blend original with denoised (favor original)
        blend_factor = 0.15  # Only 15% denoising
        result_array = (original_array * (1 - blend_factor) + denoised_array * blend_factor)
        result_array = np.clip(result_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(result_array)
    except Exception:
        return img

def apply_subtle_sharpening(img):
    """Apply very gentle sharpening to enhance clarity without artifacts"""
    try:
        # Create a very gentle unsharp mask
        blurred = img.filter(ImageFilter.GaussianBlur(radius=0.8))
        
        original_array = np.array(img).astype(np.float32)
        blurred_array = np.array(blurred).astype(np.float32)
        
        # Calculate edge detail
        detail_mask = original_array - blurred_array
        
        # Apply very subtle sharpening
        sharpening_strength = 0.25  # Much gentler than before
        sharpened_array = original_array + (detail_mask * sharpening_strength)
        sharpened_array = np.clip(sharpened_array, 0, 255).astype(np.uint8)
        
        return Image.fromarray(sharpened_array)
    except Exception:
        return img



def add_no_text_instruction(prompt):
    """Add 'no text' instruction to any prompt to ensure clean wallpapers"""
    # Add the instruction if not already present
    no_text_keywords = ['no text', 'no letters', 'no words', 'no captions']
    prompt_lower = prompt.lower()
    
    if not any(keyword in prompt_lower for keyword in no_text_keywords):
        prompt += ", no text, no letters, no words, no captions"
    
    return prompt

def main():
    parser = argparse.ArgumentParser(description="Generate AI wallpapers using Gemini-enhanced prompts and Pollinations")
    parser.add_argument("prompt", nargs='?', help="Text prompt for image generation")
    parser.add_argument("--displays", type=int, help="Number of displays (auto-detect if not specified)")
    parser.add_argument("--save-dir", help="Directory to save copies of generated images")
    parser.add_argument("--resolution", help="Image resolution (e.g., 1920x1080, 2560x1440)")
    parser.add_argument("--tool", choices=["wallpaper-cli", "m-cli", "applescript", "auto"], 
                       default="auto", help="Wallpaper setting tool to use")
    parser.add_argument("--queue-dir", default="./queued-images", help="Directory for queued wallpaper images")
    parser.add_argument("--setup", action="store_true", help="Install required dependencies")
    parser.add_argument("--generate-only", action="store_true", 
                       help="Only generate images, don't set as wallpaper")
    parser.add_argument("--private", action="store_true", 
                       help="Enable private generation mode (no prompt enhancement, minimal parameters)")
    parser.add_argument("--no-enhance", action="store_true",
                       help="Disable post-processing image enhancement effects")
    
    args = parser.parse_args()
    
    # Handle setup
    if args.setup:
        success = setup_dependencies()
        sys.exit(0 if success else 1)
    
    # Check if prompt is provided when needed
    if not args.prompt:
        print("Error: prompt is required for wallpaper generation")
        print("Use --setup flag to install dependencies without generating wallpapers")
        parser.print_help()
        sys.exit(1)
    
    # Check if requests is available (needed for Pollinations)
    try:
        import requests
    except ImportError:
        print("Error: requests library not found.")
        print("Please install it with: pip install requests --user")
        print("Or run: python3 wallpaper_generator.py --setup")
        sys.exit(1)
    
    # Determine resolution
    if args.resolution:
        try:
            width, height = map(int, args.resolution.split('x'))
        except ValueError:
            print("Invalid resolution format. Use format like: 1920x1080")
            sys.exit(1)
    else:
        # Use 5K resolution for maximum quality on macOS
        width, height = 5120, 2880  # 5K resolution - highest quality for macOS displays
    
    # Determine number of displays
    displays = args.displays or get_display_count()
    
    print(f"Generating wallpapers for {displays} display(s)")
    print(f"Resolution: {width}x{height}")
    print(f"Engine: Pollinations AI (Flux){' with Gemini enhancement' if not args.private and GEMINI_AVAILABLE else ''}")
    print(f"Post-processing: {'Enabled' if not args.no_enhance and IMAGE_PROCESSING_AVAILABLE else 'Disabled'}")
    
    # Create directories
    queue_dir = Path(args.queue_dir)
    queue_dir.mkdir(exist_ok=True)
    
    # Create a saved wallpapers directory to preserve all generated wallpapers
    saved_dir = queue_dir / "saved"
    saved_dir.mkdir(exist_ok=True)
    
    if args.save_dir:
        save_dir = Path(args.save_dir)
        save_dir.mkdir(exist_ok=True)
    
    # Generate new wallpapers
    print(f"\n=== Generating New Wallpapers ===")
    success_count = 0
    
    for display_idx in range(1, displays + 1):
        print(f"\n--- Display {display_idx} ---")
        
        # Use random seed for uniqueness and variety
        seed = random.randint(1, 2147483647)  # Use max int32 value for compatibility
        
        # Always create timestamped files to preserve wallpaper history
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Output file with timestamp to preserve all wallpapers
        if args.save_dir:
            output_file = save_dir / f"wallpaper_display_{display_idx}_{timestamp}.jpg"
        else:
            output_file = saved_dir / f"wallpaper_display_{display_idx}_{timestamp}.jpg"
        
        # Generate wallpaper
        if generate_wallpaper(args.prompt, width, height, seed, str(output_file), args.private, args.no_enhance):
            success_count += 1
            
            # Create unique queue filename to avoid caching issues
            queue_file = queue_dir / f"wallpaper_display_{display_idx}_{timestamp}.jpg"
            try:
                shutil.copy2(str(output_file), str(queue_file))
                print(f"✓ Saved timestamped copy: {output_file}")
                print(f"✓ Created queue file: {queue_file}")
            except Exception as e:
                print(f"⚠ Failed to copy to queue: {e}")
            
            # Set the newly generated wallpaper immediately (if not generate-only mode)
            if not args.generate_only:
                set_wallpaper(str(queue_file), display_idx, args.tool)
        else:
            print(f"✗ Failed to generate wallpaper for display {display_idx}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully generated {success_count}/{displays} wallpapers")
    
    # Refresh desktop after all wallpapers are set
    if success_count > 0 and not args.generate_only:
        refresh_desktop()
    
    if success_count > 0:
        print("✓ Wallpaper generation completed successfully")
        if args.generate_only:
            print("Images saved to queue directory for future use")
        else:
            print("New wallpapers have been set automatically")
    else:
        print("✗ No wallpapers were generated successfully")
        sys.exit(1)

if __name__ == "__main__":
    main()