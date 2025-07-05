#!/usr/bin/env python3
"""
High-quality wallpaper generator using Pollinations AI
Supports both direct API calls and the official pollinations package
"""

import sys
import os
import time
import requests
from urllib.parse import quote

def download_image_direct_api(prompt, width, height, seed, output_file):
    """
    Download image using direct API call to Pollinations
    """
    try:
        # URL encode the prompt
        encoded_prompt = quote(prompt)
        
        # Use flux model for highest quality with maximum resolution
        # Flux model supports up to 2048x2048 resolution
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&model=flux&nologo=true&enhance=true"
        
        print(f"Generating image with URL: {image_url}")
        
        # Make request with timeout and proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(image_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        # Write the content to file
        with open(output_file, 'wb') as file:
            file.write(response.content)
        
        # Verify file was created and has content
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Image downloaded successfully: {output_file}")
            return True
        else:
            print(f"Failed to download image: {output_file}")
            return False
            
    except Exception as e:
        print(f"Error downloading image: {str(e)}")
        return False

def download_image_with_package(prompt, width, height, seed, output_file):
    """
    Download image using the official pollinations package
    Falls back to direct API if package is not available
    """
    try:
        import pollinations
        
        # Create model with flux for highest quality
        model = pollinations.Image(
            model="flux",
            width=width,
            height=height,
            seed=seed
        )
        
        # Generate and save image
        result = model.Generate(
            prompt=prompt,
            save=True
        )
        
        # The package saves with default name, so we need to rename
        # This is a simplified implementation - the actual package behavior may vary
        if os.path.exists("generated_image.png"):
            os.rename("generated_image.png", output_file)
            print(f"Image generated successfully with pollinations package: {output_file}")
            return True
        else:
            print("Pollinations package method failed, falling back to direct API")
            return False
            
    except ImportError:
        print("Pollinations package not installed, using direct API method")
        return False
    except Exception as e:
        print(f"Error with pollinations package: {str(e)}, falling back to direct API")
        return False

def generate_wallpaper(prompt, display_index, output_file, save_dir=None):
    """
    Generate a high-quality wallpaper for a specific display
    """
    # Use current timestamp + display index as seed for uniqueness
    seed = int(time.time()) + display_index
    
    # Use maximum supported resolution for highest quality
    # Flux model supports up to 2048x2048, but we'll use 1920x1080 for standard wallpaper format
    # For ultra-high quality, you can try 2048x1152 (16:9 aspect ratio)
    width = 2048
    height = 1152  # 16:9 aspect ratio for widescreen displays
    
    print(f"Generating wallpaper for display {display_index}")
    print(f"Resolution: {width}x{height}")
    print(f"Seed: {seed}")
    print(f"Prompt: {prompt}")
    
    # Try pollinations package first, then fall back to direct API
    success = download_image_with_package(prompt, width, height, seed, output_file)
    
    if not success:
        success = download_image_direct_api(prompt, width, height, seed, output_file)
    
    # Save copy to save directory if provided
    if success and save_dir:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_filename = f"wallpaper_display_{display_index}_{timestamp}.png"
        save_path = os.path.join(save_dir, save_filename)
        
        try:
            import shutil
            shutil.copy2(output_file, save_path)
            print(f"Saved copy to: {save_path}")
        except Exception as e:
            print(f"Failed to save copy: {str(e)}")
    
    return success

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 generate_wallpaper.py '<PROMPT>' <DISPLAY_INDEX> '<OUTPUT_FILE>' [SAVE_DIR]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    display_index = int(sys.argv[2])
    output_file = sys.argv[3]
    save_dir = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
    
    success = generate_wallpaper(prompt, display_index, output_file, save_dir)
    
    if success:
        print("Wallpaper generation completed successfully")
        sys.exit(0)
    else:
        print("Wallpaper generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
