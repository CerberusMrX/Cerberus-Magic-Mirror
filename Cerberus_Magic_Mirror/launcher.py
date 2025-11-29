#!/usr/bin/env python3
# Cerberus Magic Mirror - Interactive Launcher
# Author: Sudeepa Wanigarathna

import sys
import os

# ASCII Art Banner
BANNER = """
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██████╗███████╗██████╗ ██████╗ ███████╗██████╗ ██╗   ██╗███████╗     ║
║  ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝     ║
║  ██║     █████╗  ██████╔╝██████╔╝█████╗  ██████╔╝██║   ██║███████╗     ║
║  ██║     ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██╔══██╗██║   ██║╚════██║     ║
║  ╚██████╗███████╗██║  ██║██████╔╝███████╗██║  ██║╚██████╔╝███████║     ║
║   ╚═════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ║
║                                                                          ║
║                       🎭  MAGIC MIRROR  🎭                               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

                  Author: Sudeepa Wanigarathna
                  System: Kali Linux
                  Version: 1.0.0
"""

MENU = """
┌──────────────────────────────────────────────────────────────┐
│                        MAIN MENU                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] 🚀 Launch Application                                   │
│                                                              │
│  [2] 📋 View Features & Modes                                │
│                                                              │
│  [3] 🔧 System Check                                         │
│                                                              │
│  [4] ℹ️  About & Help                                         │
│                                                              │
│  [5] 📖 Read Documentation                                   │
│                                                              │
│  [Q] ❌ Quit                                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Print the application banner."""
    clear_screen()
    print(BANNER)

def show_features():
    """Display features and modes information."""
    print("\n" + "="*70)
    print("                    FEATURES & MODES")
    print("="*70)
    print("\n🧥 MODE 1: INVISIBILITY CLOAK (ENHANCED)")
    print("   • Create an invisibility effect using color-based segmentation")
    print("   • Click-to-select: Use ANY colored cloth or towel!")
    print("   • Auto-calibration for perfect results")
    print("   • Controls: [B] Capture Background, [Click] Select Cloth")
    
    print("\n🎨 MODE 2: AIR DRAWING")
    print("   • Draw in the air by tracking a blue-colored object")
    print("   • Smooth line rendering with motion tracking")
    print("   • Create signatures, sketches, and art in real-time")
    print("   • Controls: [C] Clear Canvas")
    
    print("\n👻 MODE 3: GHOST TRAIL")
    print("   • Create mesmerizing motion trail effects")
    print("   • Adjustable trail intensity for different looks")
    print("   • Echo/ghosting effect for dynamic visuals")
    print("   • Controls: [+/-] Adjust Intensity, [R] Reset")
    
    print("\n🎨 MODE 4: COLOR PICKER (CALIBRATION)")
    print("   • Utility for finding optimal HSV color ranges")
    print("   • Visual mask preview and trackbar controls")
    print("   • Save custom settings for your lighting")
    print("   • Controls: [M] Toggle Mask, [P] Print Values")

    print("\n🖌️  MODE 5: ADVANCED PAINT MODE (NEW!)")
    print("   • Full-featured painting application")
    print("   • MS Paint-style interface with opaque sidebar")
    print("   • 12 Colors, 5 Brush sizes, 4 Eraser sizes")
    print("   • Save and Clear canvas functionality")
    print("   • Controls: [Mouse] Select tools/Draw, [U] Toggle UI")
    
    print("\n" + "="*70)
    print("GLOBAL CONTROLS:")
    print("  [1-4]  Switch Modes")
    print("  [S]    Save Snapshot")
    print("  [R]    Start/Stop Recording")
    print("  [H]    Toggle Help")
    print("  [P]    Pause")
    print("  [Q]    Quit")
    print("="*70)

def system_check():
    """Perform system checks."""
    print("\n" + "="*70)
    print("                    SYSTEM CHECK")
    print("="*70)
    
    # Check Python version
    print("\n✓ Python Version:")
    print(f"  {sys.version}")
    
    # Check dependencies
    print("\n✓ Checking Dependencies:")
    
    try:
        import cv2
        print(f"  ✅ OpenCV: {cv2.__version__}")
    except ImportError:
        print("  ❌ OpenCV: NOT INSTALLED")
        print("     Install with: pip install opencv-python")
    
    try:
        import numpy
        print(f"  ✅ NumPy: {numpy.__version__}")
    except ImportError:
        print("  ❌ NumPy: NOT INSTALLED")
        print("     Install with: pip install numpy")
    
    # Check webcam
    print("\n✓ Checking Webcam:")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"  ✅ Webcam detected: {w}x{h}")
            else:
                print("  ⚠️  Webcam detected but cannot read frames")
            cap.release()
        else:
            print("  ❌ Cannot access webcam")
            print("     Check: ls /dev/video*")
            print("     Fix permissions: sudo usermod -aG video $USER")
    except:
        print("  ❌ Error checking webcam")
    
    # Check directories
    print("\n✓ Checking Directories:")
    dirs = ['snapshots', 'recordings', 'logs', 'modes', 'utils']
    for d in dirs:
        if os.path.exists(d):
            print(f"  ✅ {d}/")
        else:
            print(f"  ⚠️  {d}/ (will be created)")
    
    # Check files
    print("\n✓ Checking Core Files:")
    files = ['main.py', 'config.py', 'requirements.txt']
    for f in files:
        if os.path.exists(f):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} MISSING!")
    
    print("\n" + "="*70)
    print("\n✓ System check complete!")
    print("  If you see any errors, please fix them before launching.")
    print("="*70)

def show_about():
    """Display about and help information."""
    print("\n" + "="*70)
    print("                    ABOUT & HELP")
    print("="*70)
    print("\n📖 CERBERUS MAGIC MIRROR")
    print("   A professional Python webcam application featuring advanced")
    print("   computer vision effects including invisibility cloaking,")
    print("   air drawing, and ghost trail effects.")
    
    print("\n👨‍💻 AUTHOR")
    print("   Sudeepa Wanigarathna")
    print("   Computer Vision & Python Enthusiast")
    
    print("\n🖥️  SYSTEM")
    print("   Developed for Kali Linux")
    print("   Compatible with most Debian-based distributions")
    
    print("\n📚 DOCUMENTATION")
    print("   README.md        - Complete project documentation")
    print("   USAGE.md         - Detailed usage guide with tutorials")
    print("   INSTALLATION.md  - Installation and troubleshooting")
    
    print("\n🔧 CONFIGURATION")
    print("   Edit config.py to customize:")
    print("   • Camera resolution and settings")
    print("   • Color detection ranges (HSV)")
    print("   • Drawing parameters and effects")
    print("   • File paths and formats")
    
    print("\n🎯 TIPS")
    print("   • Use solid, vibrant colors for best detection")
    print("   • Ensure good, even lighting")
    print("   • Capture background without any movement")
    print("   • Use Color Picker mode to calibrate colors")
    print("   • Check logs/ folder if issues occur")
    
    print("\n🌐 LEARN MORE")
    print("   OpenCV: https://docs.opencv.org/")
    print("   Python:  https://www.python.org/")
    
    print("\n" + "="*70)

def show_documentation():
    """Display documentation menu."""
    print("\n" + "="*70)
    print("                    DOCUMENTATION")
    print("="*70)
    
    docs = {
        '1': ('README.md', 'Complete project overview'),
        '2': ('USAGE.md', 'Detailed usage guide'),
        '3': ('INSTALLATION.md', 'Installation instructions'),
    }
    
    print("\nAvailable Documentation:\n")
    for key, (filename, desc) in docs.items():
        exists = "✅" if os.path.exists(filename) else "❌"
        print(f"  [{key}] {exists} {filename:20} - {desc}")
    
    print("\n  [B] Back to main menu")
    
    choice = input("\n📖 Select document to view: ").strip().lower()
    
    if choice in docs:
        filename = docs[choice][0]
        if os.path.exists(filename):
            print(f"\n📄 Opening {filename}...\n")
            os.system(f"less {filename}" if os.name == 'posix' else f"type {filename}")
        else:
            print(f"\n❌ {filename} not found!")
    
    input("\nPress Enter to continue...")

def launch_application():
    """Launch the main application."""
    print("\n" + "="*70)
    print("                  LAUNCHING APPLICATION")
    print("="*70)
    print("\n🚀 Starting Cerberus Magic Mirror...")
    print("   Press Ctrl+C to return to launcher\n")
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ ERROR: main.py not found!")
        print("   Please ensure you're in the correct directory.")
        input("\nPress Enter to continue...")
        return
    
    # Launch main application
    try:
        import main
        main.main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted. Returning to launcher...\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("   Check logs/cerberus_magic_mirror.log for details")
        input("\nPress Enter to continue...")

def main_loop():
    """Main launcher loop."""
    while True:
        print_banner()
        print(MENU)
        
        choice = input("👉 Select an option: ").strip().lower()
        
        if choice == '1':
            launch_application()
        elif choice == '2':
            clear_screen()
            print_banner()
            show_features()
            input("\n👉 Press Enter to continue...")
        elif choice == '3':
            clear_screen()
            print_banner()
            system_check()
            input("\n👉 Press Enter to continue...")
        elif choice == '4':
            clear_screen()
            print_banner()
            show_about()
            input("\n👉 Press Enter to continue...")
        elif choice == '5':
            clear_screen()
            print_banner()
            show_documentation()
        elif choice == 'q':
            print("\n👋 Thanks for using Cerberus Magic Mirror! Goodbye!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid option. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher closed. Goodbye!\n")
        sys.exit(0)
