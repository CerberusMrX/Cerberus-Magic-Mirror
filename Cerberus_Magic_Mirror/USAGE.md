# Cerberus Magic Mirror - Usage Guide

**Author:** Sudeepa Wanigarathna  
**System:** Kali Linux

This guide provides detailed instructions on how to use the Cerberus Magic Mirror application effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Mode Descriptions](#mode-descriptions)
3. [Step-by-Step Tutorials](#step-by-step-tutorials)
4. [Advanced Tips](#advanced-tips)
5. [Common Issues](#common-issues)

## Getting Started

### Launching the Application

There are two ways to start the application:

**Option 1: Using the Launcher (Recommended)**
```bash
cd Cerberus_Magic_Mirror
python launcher.py
```

The launcher provides:
- Interactive menu
- Mode selection
- Settings preview
- Help information

**Option 2: Direct Launch**
```bash
python main.py
```

This starts directly in Invisibility Cloak mode.

### First Time Setup

When you first run the application:

1. **Grant webcam permissions** if prompted
2. **Position yourself** in front of the camera
3. **Check lighting** - ensure the area is well-lit
4. **Test mode switching** - press 1, 2, 3 to try different modes

## Mode Descriptions

### Mode 1: Invisibility Cloak 🧥

**What it does:**  
Creates an invisibility effect by replacing red-colored objects with a pre-captured background.

**How it works:**
1. The application captures a background image (without you in it)
2. It detects red-colored areas in the live feed
3. It replaces those areas with the background image
4. Creates the illusion that red objects are "invisible"

**Best for:**
- Magic tricks
- Creative videos
- Invisibility demonstrations
- Harry Potter cosplay!

**Controls:**
- `B` - Capture background (step out of frame first!)

---

### Mode 2: Air Drawing 🎨

**What it does:**  
Tracks a blue-colored object and draws lines following its movement.

**How it works:**
1. Detects blue objects in the camera feed
2. Tracks the center point of the largest blue object
3. Draws a yellow line following the object's path
4. Creates persistent drawings on a virtual canvas

**Best for:**
- Air signatures
- Creative sketching
- Gesture-based art
- Educational demonstrations

**Controls:**
- `C` - Clear the canvas
- Just move your blue object to draw!

---

### Mode 3: Ghost Trail 👻

**What it does:**  
Creates a motion blur/echo effect by blending current and previous frames.

**How it works:**
1. Accumulates frames over time using weighted averaging
2. Creates a "ghosting" effect for moving objects
3. Adjustable intensity for different visual effects

**Best for:**
- Artistic videos
- Motion visualization
- Psychedelic effects
- Dance recordings

**Controls:**
- `+` / `=` - Increase trail intensity (more ghosting)
- `-` / `_` - Decrease trail intensity (less ghosting)
- `R` - Reset the accumulated frame

## Step-by-Step Tutorials

### Tutorial 1: Invisibility Cloak Effect

**What you need:**
- A red cloth, red clothing, or any red object
- Good lighting
- Stable camera position

**Steps:**

1. **Launch the application**
   ```bash
   python launcher.py
   ```

2. **Select Mode 1** (or press `1` if already running)
   - You'll see "MODE: Invisibility Cloak" at the top

3. **Step out of the camera frame completely**
   - Make sure no part of you is visible
   - Ensure the background is clean and static

4. **Press `B` to capture background**
   - You'll see "Background captured!" message
   - This image is now saved as your background

5. **Step back into frame with your red cloth**
   - Hold the red cloth in front of you
   - The red areas will show the background
   - You appear invisible behind the cloth!

6. **Move around and experiment**
   - Try different angles
   - Cover different body parts
   - Create videos with `R` key (record)

**Tips:**
- Use a **solid red color** (avoid patterns)
- Ensure **consistent lighting** before and after capturing background
- The **background should be static** (no moving objects)
- If it's not working well, recapture background with `B`

---

### Tutorial 2: Air Drawing Masterpiece

**What you need:**
- A blue object (marker cap, toy, glove, etc.)
- Contrasting background (avoid blue backgrounds)
- Good lighting

**Steps:**

1. **Launch and select Mode 2** (press `2`)
   - You'll see "MODE: Air Drawing (Track Blue Object)"

2. **Hold your blue object in view**
   - The application will detect it and draw a cyan circle around it
   - The circle indicates successful tracking

3. **Start drawing**
   - Move the object slowly and deliberately
   - You'll see a yellow line following your movements
   - The drawing persists on the canvas

4. **Create your artwork**
   - Draw shapes, write text, create patterns
   - Take your time for smooth lines

5. **Save or clear**
   - Press `S` to save a snapshot of your drawing
   - Press `C` to clear the canvas and start fresh
   - Press `R` to record a video of your drawing process

**Tips:**
- **Move slowly** for smooth, clean lines
- Use an object **at least 2-3cm in diameter**
- Ensure **good contrast** between object and background
- **Pause without clearing**: just move the object out of frame
- For **broken lines**: intentionally hide the object briefly

---

### Tutorial 3: Ghost Trail Magic

**What you need:**
- Just you!
- Preferably darker clothing for better effect
- Room to move

**Steps:**

1. **Launch and select Mode 3** (press `3`)
   - You'll see "MODE: Ghost Trail"

2. **Start with default settings**
   - The trail effect starts immediately
   - Default intensity is 0.5 (medium)

3. **Adjust the intensity**
   - Press `+` to increase ghosting (slower fade)
   - Press `-` to decrease ghosting (faster fade)
   - Experiment to find your preferred look

4. **Create effects**
   - **Slow movements:** Create long, flowing trails
   - **Fast movements:** Create multiple ghost images
   - **Dance moves:** Create artistic motion blur
   - **Hand waves:** Create mystical energy effects

5. **Reset if needed**
   - Press `R` to reset the accumulated frame
   - Starts fresh with current frame

**Tips:**
- **High intensity** (0.8-0.9): Long, persistent trails
- **Low intensity** (0.2-0.3): Short, subtle echoes
- Works best with **deliberate, fluid movements**
- Try **different lighting** for varying moods
- **Combine with colored lights** for amazing effects

## Advanced Tips

### Optimizing Color Detection

If Invisibility Cloak or Air Drawing isn't detecting colors well:

1. **Check lighting conditions**
   - Ensure even, bright lighting
   - Avoid backlighting and shadows

2. **Use solid, vibrant colors**
   - Bright red for cloak mode
   - Bright blue for drawing mode
   - Avoid pale or dark shades

3. **Adjust HSV ranges in config.py**
   ```python
   # For Cloak Mode (Red)
   CLOAK_LOWER_RED1 = [0, 120, 70]
   CLOAK_UPPER_RED1 = [10, 255, 255]
   
   # For Air Drawing (Blue)
   DRAW_LOWER_BLUE = [100, 60, 60]
   DRAW_UPPER_BLUE = [140, 255, 255]
   ```

4. **Use Color Picker Mode** (if available)
   - Launch the color picker to calibrate
   - Find the optimal HSV values for your lighting

### Recording Professional Videos

1. **Plan your shot**
   - Know what you want to capture
   - Practice movements first

2. **Set up properly**
   - Stable camera (use tripod if possible)
   - Good lighting
   - Clean background

3. **Record**
   - Press `R` to start recording
   - Red dot indicator shows recording is active
   - Press `R` again to stop

4. **Find your recordings**
   - Located in `recordings/` folder
   - Named with timestamp: `recording_YYYYMMDD-HHMMSS.avi`

### Combining Modes for Creative Effects

**Example workflow:**

1. Record an air drawing session (Mode 2)
2. Replay the video through the application
3. Apply ghost trail effect (Mode 3) in post

**Or:**

1. Set up invisibility cloak (Mode 1)
2. Switch to ghost trail (Mode 3) while "invisible"
3. Create mystical appearing/disappearing effects

## Common Issues

### Issue: Cloak effect shows wrong areas

**Solution:**
- Recapture background with `B`
- Ensure nothing moved in the background
- Check that you're using a solid red color

### Issue: Air drawing not detecting blue object

**Solution:**
- Use a brighter blue object
- Improve lighting
- Avoid blue backgrounds
- Ensure object is large enough (>10px radius)

### Issue: Ghost trail is too strong/weak

**Solution:**
- Press `+` to increase intensity
- Press `-` to decrease intensity
- Press `R` to reset and start fresh

### Issue: Application is laggy

**Solution:**
- Lower camera resolution in `config.py`
- Close other applications
- Ensure good CPU/GPU performance
- Check webcam capabilities

### Issue: Snapshots/recordings not saving

**Solution:**
- Check disk space
- Verify write permissions in project directory
- Check that `snapshots/` and `recordings/` folders exist
- Review logs in `logs/` folder

## Keyboard Reference

### Global Controls (All Modes)

| Key | Action |
|-----|--------|
| `1` | Invisibility Cloak Mode |
| `2` | Air Drawing Mode |
| `3` | Ghost Trail Mode |
| `S` | Save snapshot to `snapshots/` |
| `R` | Start/Stop video recording |
| `H` | Show help overlay |
| `P` | Pause/Resume |
| `Q` | Quit application |

### Mode-Specific Controls

**Mode 1 - Invisibility Cloak:**
- `B` - Capture background

**Mode 2 - Air Drawing:**
- `C` - Clear canvas

**Mode 3 - Ghost Trail:**
- `+` or `=` - Increase trail intensity
- `-` or `_` - Decrease trail intensity
- `R` - Reset accumulated frame

## Getting Help

If you encounter issues:

1. **Check the logs:**
   ```bash
   cat logs/cerberus_magic_mirror.log
   ```

2. **Run verification:**
   ```bash
   python verify_installation.py
   ```

3. **Check webcam:**
   ```bash
   ls /dev/video*
   v4l2-ctl --list-devices
   ```

4. **Review configuration:**
   - Check `config.py` for correct settings
   - Ensure paths exist and are writable

---

**Enjoy creating magic with Cerberus Magic Mirror! 🎭✨**

For more information, see [README.md](README.md) and [INSTALLATION.md](INSTALLATION.md).
