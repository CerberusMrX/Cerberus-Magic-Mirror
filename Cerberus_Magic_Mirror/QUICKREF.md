# Cerberus Magic Mirror - Quick Reference

**Author:** Sudeepa Wanigarathna | **System:** Kali Linux

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the application
python launcher.py

# Or run directly
python main.py
```

---

## ⌨️ Keyboard Controls

### Global Controls
| Key | Action |
|-----|--------|
| `1` | Invisibility Cloak Mode |
| `2` | Air Drawing Mode |
| `3` | Ghost Trail Mode |
| `4` | Color Picker Mode (Calibration) |
| `S` | Save Snapshot |
| `R` | Start/Stop Recording |
| `H` | Toggle Help Overlay |
| `P` | Pause/Resume |
| `Q` | Quit |

### Mode-Specific Controls

**Invisibility Cloak (Mode 1):**
- `B` - Capture Background (step out of frame first!)

**Air Drawing (Mode 2):**
- `C` - Clear Canvas

**Ghost Trail (Mode 3):**
- `+` / `=` - Increase Trail Intensity
- `-` / `_` - Decrease Trail Intensity
- `R` - Reset Effect

**Color Picker (Mode 4):**
- `M` - Toggle Mask View
- `P` - Print HSV Values
- `1-4` - Load Presets (Red, Blue, Green, Full)

---

## 📁 Project Structure

```
Cerberus_Magic_Mirror/
├── main.py              # Main application
├── launcher.py          # Interactive launcher
├── config.py            # Configuration settings
├── requirements.txt     # Dependencies
├── verify_installation.py  # Installation check
│
├── Documentation
│   ├── README.md
│   ├── USAGE.md
│   └── INSTALLATION.md
│
├── modes/               # Effect modes
│   ├── cloak_mode.py
│   ├── air_draw_mode.py
│   ├── ghost_mode.py
│   └── color_picker_mode.py
│
├── utils/               # Utilities
│   ├── overlay.py       # UI overlays
│   ├── recorder.py      # Video recording
│   └── logger.py        # Logging system
│
└── Output Directories
    ├── snapshots/       # Saved images
    ├── recordings/      # Video files
    └── logs/            # Application logs
```

---

## 🎮 Modes Overview

### 1️⃣ Invisibility Cloak
Creates invisibility effect by replacing red objects with background.
**What you need:** Red cloth/object
**Steps:**
1. Press `B` while out of frame to capture background
2. Step back in with red cloth
3. Watch the magic happen!

### 2️⃣ Air Drawing
Track a blue object to draw in the air.
**What you need:** Blue object (marker, toy, etc.)
**Steps:**
1. Hold blue object in view
2. Move to draw yellow lines
3. Press `C` to clear and start fresh

### 3️⃣ Ghost Trail
Create motion blur/echo effects.
**What you need:** Just you!
**Steps:**
1. Move around to create trails
2. Adjust intensity with `+`/`-`
3. Press `R` to reset

### 4️⃣ Color Picker
Calibrate HSV color ranges for your lighting.
**Use case:** Optimize color detection
**Steps:**
1. Adjust trackbars to find optimal values
2. Press `P` to print values
3. Update config.py with printed values

---

## ⚙️ Configuration (config.py)

### Camera Settings
```python
CAMERA_INDEX = 0         # Camera device (0 = default)
CAMERA_WIDTH = 1280      # Resolution width
CAMERA_HEIGHT = 720      # Resolution height
CAMERA_FPS = 30          # Frame rate
```

### Color Ranges (HSV)
```python
# Invisibility Cloak (Red)
CLOAK_LOWER_RED1 = [0, 120, 70]
CLOAK_UPPER_RED1 = [10, 255, 255]

# Air Drawing (Blue)
DRAW_LOWER_BLUE = [100, 60, 60]
DRAW_UPPER_BLUE = [140, 255, 255]
```

### Ghost Effect
```python
GHOST_DEFAULT_ALPHA = 0.5    # Trail intensity (0.1 - 0.9)
GHOST_ALPHA_STEP = 0.05      # Adjustment step
```

---

## 🛠️ Troubleshooting

### Webcam Not Working
```bash
# Check available cameras
ls /dev/video*

# Fix permissions
sudo usermod -aG video $USER

# Verify with v4l2
v4l2-ctl --list-devices
```

### Color Detection Issues
1. Ensure good lighting
2. Use solid, vibrant colors
3. Use Color Picker Mode (press `4`) to calibrate
4. Update config.py with found values

### Performance Issues
- Lower resolution in config.py: `CAMERA_WIDTH = 640, CAMERA_HEIGHT = 480`
- Reduce FPS: `CAMERA_FPS = 15`
- Close other applications

---

## 📍 Output Files

### Snapshots
- Location: `snapshots/`
- Format: `snapshot_YYYYMMDD-HHMMSS.jpg`
- Quality: Configurable in config.py

### Recordings
- Location: `recordings/`
- Format: `recording_YYYYMMDD-HHMMSS.avi`
- Codec: XVID (configurable)

### Logs
- Location: `logs/cerberus_magic_mirror.log`
- Contains: Session info, errors, events

---

## 🎯 Tips & Tricks

### Best Results for Invisibility Cloak
- Use **solid red color** (no patterns)
- **Static background** (no movement)
- **Consistent lighting** before and after capturing
- Recapture background if lighting changes

### Best Results for Air Drawing
- Use **bright blue object** (2-3cm diameter)
- **Move slowly** for smooth lines
- **Good contrast** with background
- Hide object briefly to break lines

### Best Results for Ghost Trail
- **Slow, deliberate movements** for long trails
- **High alpha (0.7-0.9)** for persistent trails
- **Low alpha (0.2-0.3)** for subtle echoes
- Works great with **colored lights**

---

## 📚 Documentation

- **README.md** - Complete project overview
- **USAGE.md** - Detailed tutorials and guides
- **INSTALLATION.md** - Setup and troubleshooting
- **This file** - Quick reference

---

## 🔗 Useful Commands

```bash
# Verify installation
python verify_installation.py

# Launch with launcher
python launcher.py

# Direct launch
python main.py

# Check logs
cat logs/cerberus_magic_mirror.log

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## 📊 System Requirements

**Minimum:**
- Kali Linux (or Debian-based)
- Python 3.8+
- 2GB RAM
- 480p webcam

**Recommended:**
- Python 3.10+
- 4GB RAM
- 720p+ webcam
- Good lighting

---

**For complete documentation, see README.md, USAGE.md, and INSTALLATION.md**

🎭 **Enjoy your Cerberus Magic Mirror!** ✨
