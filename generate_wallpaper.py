#!/usr/bin/env python3
"""
High-quality wallpaper generator using Pollinations AI Package
Using the pollinations pypi package
"""

import sys
import os
import time
import pollinations

def generate_wallpaper_with_pollinations(prompt, width, height, seed, output_file):
    """
    Generate wallpaper using the pollinations package
    """
    try:
        print(f"Using pollinations package to generate image...")
        
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
        
        # The package typically saves with a default name, check common patterns
        possible_files = [
            "generated_image.png",
            "image.png", 
            f"{seed}.png",
            "output.png"
        ]
        
        for possible_file in possible_files:
            if os.path.exists(possible_file):
                # Move the generated file to our desired output location
                if possible_file != output_file:
                    os.rename(possible_file, output_file)
                print(f"Image generated successfully: {output_file}")
                return True
        
        # If no standard file found, check current directory for any new PNG files
        png_files = [f for f in os.listdir('.') if f.endswith('.png')]
        if png_files:
            # Use the most recently created PNG file
            latest_file = max(png_files, key=os.path.getctime)
            os.rename(latest_file, output_file)
            print(f"Image generated successfully: {output_file}")
            return True
        
        print("Failed to locate generated image file")
        return False
        
    except Exception as e:
        print(f"Error generating image with pollinations package: {str(e)}")
        return False

def generate_wallpaper(prompt, display_index, output_file, save_dir=None):
    """
    Generate a high-quality wallpaper for a specific display
    """
    # Use current timestamp + display index as seed for uniqueness
    seed = int(time.time()) + display_index
    
    # Use high resolution for quality wallpapers
    width = 1024
    height = 1024  # Square format as shown in your example
    
    print(f"Generating wallpaper for display {display_index}")
    print(f"Resolution: {width}x{height}")
    print(f"Seed: {seed}")
    print(f"Prompt: {prompt}")
    
    # Generate wallpaper using pollinations package
    success = generate_wallpaper_with_pollinations(prompt, width, height, seed, output_file)
    
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
