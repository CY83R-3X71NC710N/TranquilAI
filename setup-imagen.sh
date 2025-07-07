#!/bin/bash
# Google Imagen-3 Setup Script for macOS AI Wallpaper Generator

echo "🎨 Setting up Google Imagen-3 for AI Wallpaper Generator"
echo "================================================="

# Check if google-imagen-3 directory exists
if [ ! -d "google-imagen-3" ]; then
    echo "❌ Error: google-imagen-3 directory not found!"
    echo "Make sure you're running this script from the main project directory."
    exit 1
fi

# Check if .env.example exists
if [ ! -f "google-imagen-3/.env.example" ]; then
    echo "❌ Error: .env.example file not found in google-imagen-3 directory!"
    exit 1
fi

echo "📋 Step 1: Getting your Google API Key"
echo "--------------------------------------"
echo "1. Visit: https://aistudio.google.com/apikey"
echo "2. Sign in with your Google account"
echo "3. Click 'Create API Key'"
echo "4. Copy the generated API key"
echo ""

# Copy .env.example to .env if it doesn't exist
if [ ! -f "google-imagen-3/.env" ]; then
    cp google-imagen-3/.env.example google-imagen-3/.env
    echo "✅ Created .env file from template"
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "📝 Step 2: Enter your API Key"
echo "-----------------------------"
read -p "Paste your Google API key here: " api_key

if [ -z "$api_key" ]; then
    echo "❌ No API key provided. You can manually edit google-imagen-3/.env later."
    echo "Replace 'your_api_key_here' with your actual API key."
else
    # Replace the placeholder in .env file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed
        sed -i '' "s/your_api_key_here/$api_key/" google-imagen-3/.env
    else
        # Linux sed
        sed -i "s/your_api_key_here/$api_key/" google-imagen-3/.env
    fi
    echo "✅ API key saved to google-imagen-3/.env"
fi

echo ""
echo "📦 Step 3: Installing Dependencies"
echo "----------------------------------"
if command -v pip3 &> /dev/null; then
    pip3 install -r google-imagen-3/requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r google-imagen-3/requirements.txt
else
    echo "❌ pip not found. Please install Python dependencies manually:"
    echo "pip install google-genai python-dotenv Pillow"
    exit 1
fi

echo ""
echo "🧪 Step 4: Testing Setup"
echo "------------------------"
echo "Testing Google Imagen-3 setup..."

# Test the setup
if python3 wallpaper_generator.py "test setup" --engine imagen --generate-only 2>/dev/null; then
    echo "✅ Google Imagen-3 setup successful!"
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo "You can now use Google Imagen-3 with:"
    echo "python3 wallpaper_generator.py \"your prompt\" --engine imagen"
    echo ""
    echo "Or use private mode with Pollinations:"
    echo "python3 wallpaper_generator.py \"your prompt\" --private"
else
    echo "⚠️  Setup may have issues. Check your API key and try:"
    echo "python3 wallpaper_generator.py \"test\" --engine imagen --generate-only"
fi

echo ""
echo "For more examples and options, see README.md"
