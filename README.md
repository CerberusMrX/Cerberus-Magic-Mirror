# 🪄 Cerberus Magic Mirror

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.5+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Professional Augmented Reality Application for Kali Linux**

*Featuring Invisibility Cloak, Gesture-Controlled Painting, and Ghost Effects*

[Features](#features) •
[Installation](#installation) •
[Usage](#usage) •
[Controls](#controls) •
[Documentation](#documentation)

---

</div>

## 📖 Overview

Cerberus Magic Mirror is a professional-grade computer vision application that brings magic to life through your webcam. Using advanced OpenCV algorithms, it provides three immersive AR experiences:

- **🎭 Invisibility Cloak** - Harry Potter-style invisibility with professional edge blending
- **🎨 AR Paint** - Gesture-controlled painting with two-finger detection  
- **👻 Ghost Trail** - Motion blur effects for ethereal visuals

Built specifically for Kali Linux, optimized for HD cameras, and designed for both entertainment and educational purposes.

---

## ✨ Features

### Mode 1: Invisibility Cloak (Professional Edition)
- ✅ **30-Frame Background Averaging** - Ultra-stable, flicker-free background
- ✅ **Click-Based Color Calibration** - Intelligent region sampling and adaptive thresholding
- ✅ **Advanced Edge Feathering** - Seamless blending with adjustable Gaussian blur (3-31px)
- ✅ **7-Frame Temporal Smoothing** - Stable mask tracking over time
- ✅ **Real-Time Adjustments** - Fine-tune edge blur on-the-fly with +/- keys

### Mode 2: AR Paint (Gesture-Controlled)
- ✅ **HD Camera Support** - 1280x720 resolution for crystal-clear visuals
- ✅ **Two-Finger Gesture Detection** - Convexity defects algorithm
  - 1 Finger = Draw mode
  - 2 Fingers = Erase mode
- ✅ **Professional Toolbar** - Compact bottom panel with 12 colors, 5 brushes, 4 erasers
- ✅ **Dual Tracking Modes** - Blue object OR finger/hand tracking
- ✅ **Dwell Click Interface** - Hover-based selection (1.2s)
- ✅ **Real-Time Feedback** - Finger count display and gesture indicators

### Mode 3: Ghost Trail
- ✅ **Adjustable Motion Blur** - Alpha blending with configurable trail length
- ✅ **Real-Time Control** - +/- keys to adjust effect strength

---

## 🚀 Installation

### Prerequisites
- **Operating System**: Kali Linux (or Debian-based distributions)
- **Python**: 3.8 or higher
- **Webcam**: Built-in or external USB camera (HD recommended)
- **Permissions**: Camera access (added to `video` group)

### Step 1: System Setup
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Add user to video group for camera access
sudo usermod -aG video $USER

# Logout and login for group changes to take effect
```

### Step 2: Install Dependencies
```bash
# Navigate to project directory
cd "Cerberus_Magic_Mirror"

# Install Python dependencies
pip3 install -r requirements.txt --break-system-packages

# Or using apt (recommended for Kali Linux)
sudo apt install python3-opencv python3-numpy -y
```

### Step 3: Verify Installation
```bash
# Run verification script
python3 verify_installation.py
```

**Expected Output:**
```
Testing modes...
Testing CloakMode...
➜ Starting background capture (30 frames)...
CloakMode OK
Testing ARPaintMode...
ARPaintMode OK
Testing GhostMode...
GhostMode OK
All tests passed!
```

### Step 4: Test Camera
```bash
# Quick camera test
python3 test_camera.py
```

---

## 📚 Usage

### Quick Start
```bash
# Launch application
python3 main.py
```

### Mode Selection
- Press **`1`** - Invisibility Cloak
- Press **`2`** - AR Paint
- Press **`3`** - Ghost Trail

---

## 🎭 Mode 1: Invisibility Cloak

### How to Use

#### Step 1: Capture Background
1. **Clear the Frame** - Step out of camera view completely
2. **Press `B`** - Start 30-frame capture
3. **Wait** - Progress bar will fill (takes ~1 second)
4. **Auto-Average** - System automatically creates stable background

#### Step 2: Calibrate Cloak
1. **Hold Cloth** - Show your cloak/cloth to camera
2. **Press `T`** - Enable calibration mode
3. **Click Color** - Click anywhere on the cloth
4. **Auto-Detect** - System samples region and calculates optimal HSV ranges

#### Step 3: Fine-Tune (Optional)
- **`+`** - Increase edge blur (smoother, more natural blending)
- **`-`** - Decrease edge blur (sharper edges)
- **`X`** - Reset everything and start over

### Tips for Best Results
- ✅ Use **solid-colored cloth** (red, green, or blue work best)
- ✅ Ensure **consistent, bright lighting** (avoid shadows)
- ✅ Keep **background static** (no movement behind)
- ✅ Avoid colors that **match skin tone or clothing**
- ✅ **Larger cloth** = better effect

### Troubleshooting
| Issue | Solution |
|-------|----------|
| Flickering effect | Increase edge blur with `+` key |
| Poor invisibility | Recalibrate color (`X` then `B` then `T`) |
| Background bleeds | Try different cloth color |
| Cloak partially visible | Ensure color is uniform and well-lit |

---

## 🎨 Mode 2: AR Paint

### Tracking Modes

#### Option A: Object Tracking (Default)
1. **Press `2`** to activate AR Paint
2. **Use blue object** (cap, marker, toy) to draw
3. **Point at toolbar** to select tools (hover 1.2s)
4. **Draw** in the main area

#### Option B: Finger Tracking (Gesture Control)
1. **Press `2`** then **`F`** to switch to finger mode
2. **Gesture Controls:**
   - **1 Finger Raised** (index) = **Drawing Mode**
   - **2 Fingers Raised** (index + middle) = **Eraser Mode**
3. **Select Tools** - Move hand to bottom toolbar, hover 1.2s
4. **Draw/Erase** - Move hand to draw with active mode

### Toolbar Layout
```
┌─────────────────────────────────────────────────────────┐
│ AR PAINT TOOLS  |  Gesture: X Fingers                   │
│ 1 Finger = Draw | 2 Fingers = Erase                     │
├─────────────────────────────────────────────────────────┤
│ [12 Colors in horizontal row]                           │
│ Brushes: [●][●][●][●][●]  Erasers: [□][□][□][□]         │
│ [CLEAR]                               [FINGER/OBJECT]   │
└─────────────────────────────────────────────────────────┘
```

### Finger Detection Requirements
- ✅ **Good Lighting** - Bright, even lighting essential
- ✅ **Plain Background** - Helps separate hand from scene
- ✅ **Palm Facing Camera** - Works best
- ✅ **Fingers Separated** - Keep fingers apart for accurate count
- ✅ **Stable Hand** - Smooth movements create clean lines

### Customization
Edit `config.py` to adjust:
```python
# Skin color range (adjust for your skin tone)
DRAW_LOWER_SKIN = [0, 30, 60]
DRAW_UPPER_SKIN = [20, 150, 255]

# Camera resolution
CAMERA_WIDTH = 1280  # HD
CAMERA_HEIGHT = 720

# Dwell time for tool selection
# (change in air_draw_mode.py line 47)
self.dwell_time = 1.2  # seconds
```

---

## 👻 Mode 3: Ghost Trail

### How to Use
1. **Press `3`** to activate
2. **Move** in front of camera to create trail effect
3. **Adjust** with `+`/`-` keys
4. **Reset** with `R` key

---

## ⌨️ Controls

### Global Controls (All Modes)
| Key | Action |
|-----|--------|
| `1` | Invisibility Cloak Mode |
| `2` | AR Paint Mode |
| `3` | Ghost Trail Mode |
| `S` | Save Snapshot |
| `R` | Record Video |
| `H` | Toggle Help Overlay |
| `P` | Pause/Resume |
| `Q` | Quit Application |

### Mode-Specific Controls

#### Invisibility Cloak
| Key | Action |
|-----|--------|
| `B` | Capture Background (30 frames) |
| `T` | Enable Calibration Mode (then click) |
| `X` | Reset Everything |
| `+` | Increase Edge Blur |
| `-` | Decrease Edge Blur |

#### AR Paint
| Key | Action |
|-----|--------|
| `F` | Toggle Finger/Object Tracking |
| `C` | Clear Canvas |
| **Mouse** | Click on toolbar items (when not using gesture mode) |
| **Gesture** | 1 Finger = Draw, 2 Fingers = Erase |

#### Ghost Trail
| Key | Action |
|-----|--------|
| `+` | Increase Trail Length |
| `-` | Decrease Trail Length |
| `R` | Reset Effect |

---

## 📁 File Structure

```
Cerberus_Magic_Mirror/
├── main.py                    # Main application entry point
├── config.py                  # Configuration (colors, camera, UI)
├── requirements.txt           # Python dependencies
├── verify_installation.py     # Installation verification script
├── test_camera.py            # Camera connectivity test
├── modes/                    
│   ├── base_mode.py          # Base class for all modes
│   ├── cloak_mode.py         # Invisibility Cloak implementation
│   ├── air_draw_mode.py      # AR Paint with gesture control
│   └── ghost_mode.py         # Ghost Trail effect
├── utils/
│   ├── overlay.py            # UI overlay utilities
│   ├── recorder.py           # Video recording
│   └── logger.py             # Logging system
├── snapshots/                # Saved snapshots
├── recordings/               # Recorded videos
└── logs/                     # Application logs
```

---

## 🔧 Technical Details

### Invisibility Cloak Algorithm
1. **Background Capture**: Median filter over 30 frames for stability
2. **Color Detection**: HSV color space with dual-range thresholding (for red)
3. **Mask Refinement**: Morphological operations (OPEN + CLOSE + DILATE)
4. **Temporal Smoothing**: 7-frame moving average of masks
5. **Edge Feathering**: Configurable Gaussian blur (21px default)
6. **Alpha Blending**: Smooth transitions with boundary-specific blur

### Finger Detection Algorithm
1. **Skin Segmentation**: HSV-based skin color detection
2. **Contour Analysis**: Find largest contour (hand)
3. **Convex Hull**: Compute convex hull of hand contour
4. **Convexity Defects**: Find defects (gaps between fingers)
5. **Angle Calculation**: Measure angles at defects using law of cosines
6. **Finger Counting**: Count defects with angle < 90° and depth > threshold
7. **Fingertip Detection**: Topmost point of convex hull

### Performance
- **Resolution**: 1280x720 (HD)
- **Frame Rate**: ~30 FPS (depends on system)
- **Latency**: < 50ms
- **Memory Usage**: ~200-300MB
- **CPU Usage**: Moderate (OpenCV is optimized)

---

## 🐛 Troubleshooting

### Camera Issues

#### "Could not open webcam"
```bash
# Check camera devices
ls /dev/video*

# Test camera with fswebcam
sudo apt install fswebcam
fswebcam test.jpg

# Check permissions
groups $USER  # Should include 'video'

# Try different camera index in config.py
CAMERA_INDEX = 0  # Try 1, 2, etc.
```

#### "Camera busy" error
```bash
# Close other applications using camera
# Check running processes
lsof /dev/video0

# Kill process if needed
sudo killall cheese  # or other camera app
```

### Performance Issues

#### Low FPS
- Reduce resolution in `config.py`:
  ```python
  CAMERA_WIDTH = 640
  CAMERA_HEIGHT = 480
  ```
- Use Object mode instead of Finger mode
- Close other applications

#### High CPU Usage
- Normal for real-time CV processing
- Reduce resolution or FPS if needed

### Finger Detection Issues

#### Fingers Not Detected
1. **Improve Lighting** - Use bright, even lighting
2. **Adjust Skin Range** - Edit `config.py`:
   ```python
   # For darker skin
   DRAW_LOWER_SKIN = [0, 20, 40]
   
   # For lighter skin  
   DRAW_UPPER_SKIN = [25, 170, 255]
   ```
3. **Use Plain Background** - White or solid-colored wall works best
4. **Check Hand Position** - Palm facing camera, fingers separated

#### Wrong Finger Count
- Ensure good lighting
- Separate fingers clearly
- Keep hand stable
- Try adjusting detection threshold in `air_draw_mode.py` (line 74):
  ```python
  if angle <= np.pi / 2 and d > 8000:  # Lower for more sensitivity
  ```

---

## 📝 Configuration

Edit `config.py` to customize:

### Camera Settings
```python
CAMERA_INDEX = 0        # Camera device number
CAMERA_WIDTH = 1280     # Resolution width
CAMERA_HEIGHT = 720     # Resolution height
CAMERA_FPS = 30         # Frames per second
```

### Invisibility Cloak
```python
# Red cloth detection (default)
CLOAK_LOWER_RED1 = [0, 120, 70]
CLOAK_UPPER_RED1 = [10, 255, 255]
CLOAK_LOWER_RED2 = [170, 120, 70]
CLOAK_UPPER_RED2 = [180, 255, 255]
```

### AR Paint
```python
# Blue object detection
DRAW_LOWER_BLUE = [100, 60, 60]
DRAW_UPPER_BLUE = [140, 255, 255]

# Finger/skin detection
DRAW_LOWER_SKIN = [0, 30, 60]
DRAW_UPPER_SKIN = [20, 150, 255]

# Colors available in toolbar
PAINT_COLORS = [
    (255, 255, 255),  # White
    (0, 0, 0),        # Black
    (0, 0, 255),      # Red
    # ... more colors
]
```

---

## 🎓 Advanced Usage

### Recording Videos
1. **Press `R`** to start recording
2. Red indicator appears in top-right
3. **Press `R`** again to stop
4. Video saved to `recordings/` folder with timestamp

### Taking Snapshots
- **Press `S`** to capture current frame
- Saved to `snapshots/` folder with timestamp
- Format: JPG (configurable in `config.py`)

### Logging
- Application logs saved to `logs/cerberus_magic_mirror.log`
- Change log level in `config.py`:
  ```python
  LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR
  ```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Sudeepa Wanigarathna**
- Platform: Kali Linux
- Version: 2.0 Professional Edition
- Date: November 2025

---

## 🙏 Acknowledgments

- OpenCV community for excellent documentation
- Kali Linux team for a robust platform
- All contributors and testers

---

## 📞 Support

Having issues? Try these resources:
1. Check [Troubleshooting](#troubleshooting) section
2. Review `logs/cerberus_magic_mirror.log`
3. Run `python3 verify_installation.py`
4. Open an issue on GitHub

---

## 🔮 Future Enhancements

Planned features:
- [ ] MediaPipe Hands integration for improved finger tracking
- [ ] Multi-color cloak support
- [ ] Shape drawing tools (circle, rectangle, line)
- [ ] Undo/Redo functionality
- [ ] Custom gesture mapping
- [ ] Background image selection
- [ ] Export drawings as PNG
- [ ] 3-finger gestures for special actions

---

<div align="center">

**Made with ❤️ and OpenCV**

*Star ⭐ this repo if you find it useful!*

</div>
