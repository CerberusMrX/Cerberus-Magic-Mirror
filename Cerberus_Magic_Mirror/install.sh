#!/bin/bash
# Cerberus Magic Mirror - Installation Helper
# This script helps install dependencies on Kali Linux

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   Cerberus Magic Mirror - Installation Helper               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Kali/Debian
if [ -f /etc/debian_version ]; then
    echo "✓ Debian-based system detected"
else
    echo "⚠ Warning: Not a Debian-based system"
fi

echo ""
echo "Choose installation method:"
echo ""
echo "  [1] System packages (recommended for Kali Linux)"
echo "      Installs: python3-opencv python3-numpy"
echo "      Requires: sudo privileges"
echo ""
echo "  [2] Virtual environment (recommended for development)"
echo "      Creates venv and installs packages locally"
echo "      No sudo required"
echo ""
echo "  [3] Check if already installed"
echo ""
echo "  [Q] Quit"
echo ""

read -p "Select option [1/2/3/Q]: " choice

case $choice in
    1)
        echo ""
        echo "Installing system packages..."
        echo "You will be prompted for your password."
        sudo apt update
        sudo apt install -y python3-opencv python3-numpy
        echo ""
        echo "✓ System packages installed!"
        ;;
    2)
        echo ""
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "✓ Virtual environment created"
        
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        echo "Installing packages..."
        pip install --upgrade pip
        pip install -r requirements.txt
        echo ""
        echo "✓ Packages installed in virtual environment!"
        echo ""
        echo "To use the application:"
        echo "  1. Activate venv: source venv/bin/activate"
        echo "  2. Run: python launcher.py"
        echo "  3. Deactivate when done: deactivate"
        ;;
    3)
        echo ""
        echo "Checking installation..."
        python3 -c "import cv2; import numpy; print('✓ OpenCV version:', cv2.__version__); print('✓ NumPy version:', numpy.__version__)" 2>/dev/null && echo "" && echo "✓ All dependencies are installed!" || echo "✗ Dependencies not found. Please install using option 1 or 2."
        ;;
    [Qq])
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Next steps:"
echo "  • Run verification: python3 verify_installation.py"
echo "  • Launch application: python3 launcher.py"
echo "════════════════════════════════════════════════════════════════"
