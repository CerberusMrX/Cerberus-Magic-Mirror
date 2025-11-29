# Cerberus Magic Mirror - Configuration
# Author: Sudeepa Wanigarathna

"""
Configuration file for Cerberus Magic Mirror.
Adjust these settings to customize the application behavior.
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================

# Camera Device
CAMERA_INDEX = 0  # 0 for default webcam, 1+ for additional cameras

# Resolution
CAMERA_WIDTH = 640  # Standard resolution for compatibility
CAMERA_HEIGHT = 480  # 480p

# Frame Rate
CAMERA_FPS = 30  # Frames per second (15, 30, 60)

# ============================================================================
# COLOR DETECTION SETTINGS (HSV Color Space)
# ============================================================================

# Invisibility Cloak Mode - Red Color Detection
# Red wraps around in HSV, so we need two ranges
CLOAK_LOWER_RED1 = [0, 120, 70]
CLOAK_UPPER_RED1 = [10, 255, 255]
CLOAK_LOWER_RED2 = [170, 120, 70]
CLOAK_UPPER_RED2 = [180, 255, 255]

# Air Drawing Mode - Blue Color Detection
DRAW_LOWER_BLUE = [100, 60, 60]
DRAW_UPPER_BLUE = [140, 255, 255]

# Skin Color Detection (Approximate)
DRAW_LOWER_SKIN = [0, 20, 70]
DRAW_UPPER_SKIN = [20, 255, 255]

# ============================================================================
# AIR DRAWING SETTINGS
# ============================================================================

# Drawing Parameters
DRAW_COLOR = (0, 255, 255)  # BGR: Yellow
DRAW_THICKNESS = 5  # Line thickness in pixels
DRAW_MAX_POINTS = 512  # Maximum points to remember

# Detection Threshold
DRAW_MIN_RADIUS = 10  # Minimum object radius to detect (in pixels)

# ============================================================================
# GHOST TRAIL SETTINGS
# ============================================================================

# Default alpha value for frame blending (0.0 to 1.0)
# Higher = longer trails, Lower = shorter trails
GHOST_DEFAULT_ALPHA = 0.5

# Alpha adjustment step
GHOST_ALPHA_STEP = 0.05

# Alpha limits
GHOST_MIN_ALPHA = 0.1
GHOST_MAX_ALPHA = 0.9

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Directory paths
SNAPSHOT_DIR = "snapshots"
RECORDING_DIR = "recordings"
LOG_DIR = "logs"
ASSETS_DIR = "assets"

# Snapshot format
SNAPSHOT_FORMAT = "jpg"  # jpg, png
SNAPSHOT_QUALITY = 95  # 0-100 for jpg

# Recording settings
RECORDING_CODEC = "XVID"  # XVID, MJPG, MP4V
RECORDING_FPS = 20  # Recording framerate
RECORDING_FORMAT = "avi"  # avi, mp4

# ============================================================================
# UI OVERLAY SETTINGS
# ============================================================================

# Text Properties
UI_FONT_SCALE = 0.7
UI_FONT_THICKNESS = 2
UI_FONT_COLOR = (255, 255, 255)  # White
UI_FONT_BG_COLOR = (0, 0, 0)  # Black

# Mode Name Display
MODE_NAME_SCALE = 1.0
MODE_NAME_COLOR = (0, 255, 255)  # Cyan
MODE_NAME_POSITION = (20, 40)

# Recording Indicator
RECORDING_INDICATOR_COLOR = (0, 0, 255)  # Red
RECORDING_INDICATOR_SIZE = 15

# FPS Counter
SHOW_FPS = False  # Set to True to display FPS
FPS_POSITION = (20, 80)
FPS_COLOR = (0, 255, 0)  # Green

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Morphology kernel size for color detection
MORPH_KERNEL_SIZE = 3

# Erosion/Dilation iterations for noise reduction
EROSION_ITERATIONS = 2
DILATION_ITERATIONS = 2

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Log file
LOG_FILENAME = "cerberus_magic_mirror.log"

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Mirror effect (flip horizontally)
MIRROR_EFFECT = True

# Wait key delay (milliseconds)
WAITKEY_DELAY = 1

# Window name
WINDOW_NAME = "Cerberus Magic Mirror"

# ============================================================================
# ADVANCED PAINT MODE SETTINGS
# ============================================================================

# Color Palette (BGR format)
PAINT_COLORS = [
    (255, 255, 255),  # White
    (0, 0, 0),        # Black
    (0, 0, 255),      # Red
    (0, 255, 0),      # Green
    (255, 0, 0),      # Blue
    (0, 255, 255),    # Yellow
    (255, 0, 255),    # Magenta
    (255, 165, 0),    # Orange
    (128, 0, 128),    # Purple
    (0, 128, 128),    # Teal
    (255, 192, 203),  # Pink
    (165, 42, 42),    # Brown
]

# Brush sizes
PAINT_BRUSH_SIZES = [2, 5, 10, 15, 20]

# Eraser sizes
PAINT_ERASER_SIZES = [10, 20, 30, 50]

# UI positions
PAINT_PALETTE_X = 10
PAINT_PALETTE_Y = 80
PAINT_COLOR_SIZE = 30
PAINT_COLOR_SPACING = 5

# ============================================================================
# HELP TEXT
# ============================================================================

HELP_TEXT = [
    "=== CERBERUS MAGIC MIRROR ===",
    "",
    "GLOBAL CONTROLS:",
    "  [1] - Invisibility Cloak (Best)",
    "  [2] - AR Paint (Full AR)",
    "  [3] - Ghost Trail",
    "  [S] - Save Snapshot",
    "  [R] - Start/Stop Recording",
    "  [H] - Toggle Help",
    "  [P] - Pause",
    "  [Q] - Quit",
    "",
    "MODE CONTROLS:",
    "  Cloak: [B] Capture (30 frames)",
    "         [T] Calibrate  [X] Reset",
    "         [+/-] Edge Blur",
    "  AR Paint: [Hover] Select Tool",
    "            [F] Toggle Finger/Object",
    "            [C] Clear Canvas",
    "  Ghost: [+/-] Adjust Trail",
    "         [R] Reset Effect",
    "",
    "Press [H] to hide this help",
]

# ============================================================================
# END OF CONFIGURATION
# ============================================================================
