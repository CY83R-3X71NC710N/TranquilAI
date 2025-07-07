#!/usr/bin/env python3
"""
Test script for Gemini response parsing
"""

def parse_gemini_response(response_text):
    """
    Parse Gemini response to extract the best option when multiple are provided.
    Sometimes Gemini provides multiple options despite instructions to provide only one.
    """
    try:
        # Check if response contains multiple options
        if "**Option" in response_text or "Option 1" in response_text:
            print("  Multiple options detected, selecting the first one...")
            
            # Look for patterns like "**Option 1 (Title):**" or "Option 1:"
            import re
            
            # First try to find the content between quotes for Option 1
            option_pattern = r'\*\*Option\s+1[^:]*:\*\*\s*\n?\s*"([^"]+)"'
            match = re.search(option_pattern, response_text, re.DOTALL)
            
            if match:
                selected_option = match.group(1).strip()
                print(f"  ✓ Selected: Option 1")
                return selected_option
            
            # Alternative pattern without quotes but with clear option boundary
            option_pattern = r'\*\*Option\s+1[^:]*:\*\*\s*\n?\s*([^*]+?)(?=\*\*Option\s+2|\n\*\*|$)'
            match = re.search(option_pattern, response_text, re.DOTALL)
            
            if match:
                selected_option = match.group(1).strip()
                # Clean up any trailing text or formatting
                lines = selected_option.split('\n')
                # Take the first non-empty line or combine multiple lines if it's a paragraph
                if lines:
                    if len(lines) == 1:
                        selected_option = lines[0].strip()
                    else:
                        # For multi-line descriptions, clean and join
                        cleaned_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('**')]
                        selected_option = ' '.join(cleaned_lines)
                print(f"  ✓ Selected: Option 1")
                return selected_option
            
            # Fallback: split by lines and take first substantial content after "Option 1"
            lines = response_text.split('\n')
            capture_next = False
            collected_lines = []
            
            for line in lines:
                if "Option 1" in line:
                    capture_next = True
                    continue
                elif capture_next:
                    if line.strip():
                        if line.startswith("**Option 2") or line.startswith("Option 2"):
                            break  # Stop at Option 2
                        if not line.startswith("**") and not line.startswith("Option"):
                            # Remove quotes if present and clean the line
                            clean_line = line.strip().strip('"')
                            if clean_line:
                                collected_lines.append(clean_line)
                    elif collected_lines:  # Empty line after collecting content
                        break
            
            if collected_lines:
                selected_option = ' '.join(collected_lines)
                print(f"  ✓ Selected: Option 1 (fallback method)")
                return selected_option
        
        # If no multiple options detected, return the original response
        return response_text.strip()
        
    except Exception as e:
        print(f"  ⚠ Error parsing Gemini response: {str(e)}")
        print("  Using original response")
        return response_text.strip()

# Test with the example from user's problem
test_response = '''**Option 1 (Epic Fantasy):**

"A colossal, ethereal giant, sculpted from ancient granite and verdant moss, stands silhouetted against a dramatic, swirling twilight sky. Wisps of luminous fog curl around his colossal legs, obscuring the lower landscape. Emphasize a sense of overwhelming scale and ancient power. Lighting is key: rim light from the setting sun creates a vibrant halo around his form, highlighting the intricate textures of his earthen skin. Panoramic composition, ideal for widescreen desktop wallpaper. Fantasy art, digital painting, photorealistic detail. NO TEXT."

**Option 2 (Sci-Fi/Cyberpunk):**

"A monolithic cyborg, a bio-engineered giant, looms above a dystopian cityscape. Neon lights reflect off polished chrome and rain-slicked streets, creating a vibrant, cyberpunk aesthetic. Steam vents and glowing energy conduits accentuate the sheer power and scale of this future-age behemoth. Ultra-detailed textures, volumetric lighting, cinematic composition. Dark blues, vibrant oranges, and hints of toxic green. Wide-angle, low perspective. Sci-fi concept art, photorealistic rendering, 8K resolution. NO TEXT."'''

print("Testing Gemini response parsing...")
print(f"Original response length: {len(test_response)} characters")
print()

result = parse_gemini_response(test_response)
print()
print(f"Parsed result: {result}")
print(f"Parsed length: {len(result)} characters")
