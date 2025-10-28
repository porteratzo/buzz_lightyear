#!/bin/bash
# Installation script for Buzz Lightyear Costume Controller

echo "========================================"
echo "Buzz Lightyear Controller Installation"
echo "========================================"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    echo "   Installation will continue, but GPIO features won't work"
    echo ""
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "✗ pip3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi
echo "✓ pip3 is installed"

# Install system dependencies
echo ""
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev python3-rpi.gpio

# Install Python packages
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create audio directory if it doesn't exist
if [ ! -d "audio" ]; then
    mkdir -p audio
    echo "✓ Created audio directory"
fi

# Check if config.py exists, if not copy from example
if [ ! -f "config.py" ]; then
    cp config_example.py config.py
    echo "✓ Created config.py from config_example.py"
else
    echo "✓ config.py already exists"
fi

# Make scripts executable
chmod +x buzz_controller.py
chmod +x test_controller.py
echo "✓ Made scripts executable"

echo ""
echo "========================================"
echo "Installation Complete! 🚀"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Add audio files to the 'audio/' directory (see audio/README.md)"
echo "2. Review and adjust config.py if needed"
echo "3. Wire up your hardware according to WIRING.md"
echo "4. Test the controller:"
echo "   python3 test_controller.py"
echo "5. Run the controller:"
echo "   sudo python3 buzz_controller.py"
echo ""
echo "Note: Run with sudo to access GPIO pins"
echo ""
echo "To infinity and beyond! ✨"
