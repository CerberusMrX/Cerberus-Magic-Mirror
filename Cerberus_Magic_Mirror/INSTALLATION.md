# Cerberus Magic Mirror - Installation Guide

**Author:** Sudeepa Wanigarathna  
**System:** Kali Linux

This guide provides step-by-step instructions for installing and setting up Cerberus Magic Mirror on your Kali Linux system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Webcam Setup](#webcam-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

Before installing Cerberus Magic Mirror, ensure you have:

- **Kali Linux** (or any Debian-based distribution)
- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Webcam** (built-in or USB)
- **Git** (optional, for cloning)

### Check Python Version

```bash
python3 --version
```

Expected output: `Python 3.8.x` or higher

If Python is not installed:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## System Requirements

### Minimum Requirements
- **OS:** Kali Linux 2020.1 or later
- **CPU:** Dual-core processor, 1.5 GHz
- **RAM:** 2 GB
- **Storage:** 500 MB free space
- **Webcam:** 480p (VGA) minimum

### Recommended Requirements
- **OS:** Kali Linux 2023.x or later
- **CPU:** Quad-core processor, 2.0 GHz or higher
- **RAM:** 4 GB or more
- **Storage:** 1 GB free space
- **Webcam:** 720p (HD) or higher

## Installation Steps

### Step 1: Download the Project

**Option A: Using Git (Recommended)**
```bash
# Navigate to your desired directory
cd ~/Desktop

# Clone the repository (if hosted on Git)
git clone <repository-url> Cerberus_Magic_Mirror

# Or download and extract if you have a ZIP file
```

**Option B: Manual Download**
- Download the project ZIP file
- Extract to your desired location
- Rename folder to `Cerberus_Magic_Mirror`

### Step 2: Navigate to Project Directory

```bash
cd Cerberus_Magic_Mirror
```

### Step 3: Create Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your terminal should now show (venv) prefix
```

### Step 4: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

This will install:
- **opencv-python** - Computer vision library
- **numpy** - Numerical computing library

### Step 5: Create Output Directories

The application needs directories for saving snapshots and recordings:

```bash
# Create directories if they don't exist
mkdir -p snapshots recordings logs assets
```

### Step 6: Verify Installation

Run the verification script to ensure everything is set up correctly:

```bash
python verify_installation.py
```

**Expected Output:**
```
Testing modes...
Testing CloakMode...
CloakMode OK
Testing AirDrawMode...
AirDrawMode OK
Testing GhostMode...
GhostMode OK
Testing Overlay...
Overlay OK
All tests passed!
```

If all tests pass, your installation is successful! ✅

## Webcam Setup

### Check Webcam Availability

```bash
# List available video devices
ls /dev/video*
```

**Expected output:**
```
/dev/video0
```

If you have multiple webcams, you may see `/dev/video0`, `/dev/video1`, etc.

### Test Webcam Access

```bash
# List detailed device information
v4l2-ctl --list-devices
```

If `v4l2-ctl` is not installed:
```bash
sudo apt install v4l-utils
```

### Grant Webcam Permissions

Add your user to the video group:

```bash
# Add user to video group
sudo usermod -aG video $USER

# Log out and log back in for changes to take effect
# Or use:
newgrp video
```

### Test Webcam with OpenCV

Quick test to ensure OpenCV can access your webcam:

```bash
python3 << EOF
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Webcam is accessible!")
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame captured: {frame.shape}")
    cap.release()
else:
    print("❌ Cannot access webcam")
EOF
```

## Verification

### Run the Application

```bash
# Using launcher (recommended)
python launcher.py

# Or directly
python main.py
```

### What to Expect

1. **Webcam indicator light** should turn on
2. **Application window** should open showing live feed
3. **Mode name** should be displayed at top: "MODE: Invisibility Cloak"
4. **Controls** should be visible at the bottom

### Test Basic Functionality

1. **Mode Switching:**
   - Press `1` - Should switch to Invisibility Cloak
   - Press `2` - Should switch to Air Drawing
   - Press `3` - Should switch to Ghost Trail

2. **Snapshot:**
   - Press `S` - Should save a snapshot
   - Check `snapshots/` folder for the image

3. **Quit:**
   - Press `Q` - Should close the application cleanly

If all these work, installation is complete! 🎉

## Troubleshooting

### Issue: "No module named cv2"

**Cause:** OpenCV not installed properly

**Solution:**
```bash
pip install opencv-python --upgrade
```

### Issue: "No module named numpy"

**Cause:** NumPy not installed

**Solution:**
```bash
pip install numpy --upgrade
```

### Issue: "Error: Could not open webcam"

**Possible causes and solutions:**

1. **Webcam not connected**
   ```bash
   ls /dev/video*
   # Should show at least /dev/video0
   ```

2. **Permission denied**
   ```bash
   sudo usermod -aG video $USER
   newgrp video
   ```

3. **Webcam in use by another application**
   - Close other applications using webcam (Cheese, Skype, etc.)
   - Kill conflicting processes:
   ```bash
   sudo fuser /dev/video0
   # Then kill the process ID shown
   ```

4. **Wrong device index**
   - Edit `main.py` and try different camera indices:
   ```python
   cap = cv2.VideoCapture(1)  # Try 1 instead of 0
   ```

### Issue: Import errors for modes or utils

**Cause:** Python path issues

**Solution:**
```bash
# Ensure you're in the project root directory
cd /path/to/Cerberus_Magic_Mirror

# Run with Python module syntax
python -m main
```

### Issue: Poor performance / Low FPS

**Solutions:**

1. **Lower resolution in config.py:**
   ```python
   CAMERA_WIDTH = 640
   CAMERA_HEIGHT = 480
   ```

2. **Close other applications:**
   ```bash
   # Check CPU usage
   htop
   # Close unnecessary processes
   ```

3. **Update OpenCV:**
   ```bash
   pip install opencv-python --upgrade
   ```

### Issue: "Permission denied" when saving snapshots

**Cause:** No write permission in directory

**Solution:**
```bash
# Ensure directories exist and are writable
mkdir -p snapshots recordings logs
chmod 755 snapshots recordings logs
```

### Issue: Virtual environment activation fails

**On some systems:**
```bash
# If 'source venv/bin/activate' doesn't work, try:
. venv/bin/activate

# Or use:
bash venv/bin/activate
```

## Additional Configuration

### Setting Custom Camera Resolution

Edit `config.py`:

```python
# Camera Settings
CAMERA_WIDTH = 1280  # Change to your preferred width
CAMERA_HEIGHT = 720  # Change to your preferred height
CAMERA_FPS = 30      # Frames per second
```

### Setting Custom Color Ranges

If color detection doesn't work well in your lighting:

Edit `config.py`:

```python
# Invisibility Cloak - Red color range (HSV)
CLOAK_LOWER_RED1 = [0, 120, 70]
CLOAK_UPPER_RED1 = [10, 255, 255]

# Air Drawing - Blue color range (HSV)
DRAW_LOWER_BLUE = [100, 60, 60]
DRAW_UPPER_BLUE = [140, 255, 255]
```

## Updating the Application

```bash
# Navigate to project directory
cd Cerberus_Magic_Mirror

# Activate virtual environment if using one
source venv/bin/activate

# Pull latest changes (if using Git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Verify installation
python verify_installation.py
```

## Uninstallation

To remove Cerberus Magic Mirror:

```bash
# Deactivate virtual environment if active
deactivate

# Remove the project directory
rm -rf /path/to/Cerberus_Magic_Mirror

# Remove virtual environment (if created separately)
rm -rf /path/to/venv
```

## Getting Help

If you encounter issues not covered here:

1. **Check the logs:**
   ```bash
   cat logs/cerberus_magic_mirror.log
   ```

2. **Verify OpenCV installation:**
   ```bash
   python3 -c "import cv2; print(cv2.__version__)"
   ```

3. **Check system resources:**
   ```bash
   free -h    # Check RAM
   df -h      # Check disk space
   htop       # Check CPU usage
   ```

4. **Review error messages carefully** - they often indicate the exact problem

## Next Steps

After successful installation:

1. **Read the [USAGE.md](USAGE.md)** guide for detailed usage instructions
2. **Experiment with different modes** to understand capabilities
3. **Customize settings** in `config.py` to match your environment
4. **Create your first invisibility video!** 🎭

---

**Installation complete! Enjoy your Cerberus Magic Mirror! ✨**

For more information, see [README.md](README.md) and [USAGE.md](USAGE.md).
