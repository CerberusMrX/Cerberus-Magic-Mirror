import cv2
import numpy as np
from .base_mode import BaseMode
import config

class GhostMode(BaseMode):
    def __init__(self):
        self.accumulated_frame = None
        self.alpha = config.GHOST_DEFAULT_ALPHA  # Blending factor from config

    def process_frame(self, frame):
        if self.accumulated_frame is None:
            self.accumulated_frame = frame.astype("float")
            return frame

        # Calculate weighted average
        cv2.accumulateWeighted(frame, self.accumulated_frame, self.alpha)
        
        # Convert back to uint8
        result = cv2.convertScaleAbs(self.accumulated_frame)
        return result

    def handle_input(self, key):
        # Increase alpha (more ghosting)
        if key == ord('+') or key == ord('='):
            self.alpha = min(config.GHOST_MAX_ALPHA, self.alpha + config.GHOST_ALPHA_STEP)
            print(f"Trail intensity increased: {self.alpha:.2f}")
        
        # Decrease alpha (less ghosting)
        elif key == ord('-') or key == ord('_'):
            self.alpha = max(config.GHOST_MIN_ALPHA, self.alpha - config.GHOST_ALPHA_STEP)
            print(f"Trail intensity decreased: {self.alpha:.2f}")
        
        # Reset accumulated frame
        elif key == ord('r') or key == ord('R'):
            self.accumulated_frame = None
            print("Ghost effect reset")

    def get_name(self):
        return f"Ghost Trail (Intensity: {self.alpha:.2f})"

    def get_controls(self):
        return [
            ("+/-", "Adjust Trail Intensity"),
            ("R", "Reset Effect")
        ]
