import cv2
import numpy as np
import time
from collections import deque
from .base_mode import BaseMode
import config

def draw_text_with_outline(frame, text, position, font_scale=0.8, thickness=2, text_color=(255, 255, 255), outline_color=(0, 0, 0), outline_thickness=4):
    """Draw text with black outline for better visibility."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Draw outline
    cv2.putText(frame, text, position, font, font_scale, outline_color, thickness + outline_thickness, cv2.LINE_AA)
    # Draw main text
    cv2.putText(frame, text, position, font, font_scale, text_color, thickness, cv2.LINE_AA)

class CloakMode(BaseMode):
    def __init__(self):
        # Background capture with multi-frame averaging
        self.background = None
        self.background_frames = deque(maxlen=30)
        self.is_capturing_background = False
        self.background_capture_count = 0
        self.background_capture_target = 30
        
        # Default to config red color ranges
        self.lower_color1 = np.array(config.CLOAK_LOWER_RED1)
        self.upper_color1 = np.array(config.CLOAK_UPPER_RED1)
        self.lower_color2 = np.array(config.CLOAK_LOWER_RED2)
        self.upper_color2 = np.array(config.CLOAK_UPPER_RED2)
        self.use_dual_range = True
        
        # Click-to-select mode
        self.calibration_mode = False
        self.selected_point = None
        self.selected_color = None
        
        # Advanced settings for BEST quality
        self.mask_history = deque(maxlen=7)  # Increased for even smoother temporal smoothing
        self.edge_blur_size = 21  # Optimal default for smooth edges
        self.morph_kernel_size = 9  # Larger for better noise removal
        
        # Additional enhancement
        self.background_blur_amount = 0  # Optional background blur for depth effect
        
    def calibrate_from_click(self, frame, x, y):
        """Calibrate color range from clicked point with improved accuracy."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Sample a larger region for even better accuracy
        sample_size = 15
        x1, y1 = max(0, x-sample_size), max(0, y-sample_size)
        x2, y2 = min(frame.shape[1], x+sample_size), min(frame.shape[0], y+sample_size)
        region = hsv[y1:y2, x1:x2]
        
        # Calculate mean and std of the region
        h_mean = np.mean(region[:,:,0])
        s_mean = np.mean(region[:,:,1])
        v_mean = np.mean(region[:,:,2])
        
        h_std = np.std(region[:,:,0])
        s_std = np.std(region[:,:,1])
        v_std = np.std(region[:,:,2])
        
        # Store the selected color
        self.selected_color = frame[y, x].copy()
        
        # Adaptive tolerance
        h_tolerance = max(18, int(h_std * 2.5))
        s_tolerance = max(50, int(s_std * 2.5))
        v_tolerance = max(50, int(v_std * 2.5))
        
        print(f"✓ Color calibrated! HSV: ({int(h_mean)}, {int(s_mean)}, {int(v_mean)})")
        print(f"  Tolerance: H±{h_tolerance}, S±{s_tolerance}, V±{v_tolerance}")
        
        # Check if it's red (wraps around in HSV)
        if h_mean < 20 or h_mean > 160:
            self.use_dual_range = True
            self.lower_color1 = np.array([0, max(20, s_mean - s_tolerance), max(20, v_mean - v_tolerance)])
            self.upper_color1 = np.array([20, 255, 255])
            self.lower_color2 = np.array([160, max(20, s_mean - s_tolerance), max(20, v_mean - v_tolerance)])
            self.upper_color2 = np.array([180, 255, 255])
        else:
            self.use_dual_range = False
            self.lower_color1 = np.array([
                max(0, h_mean - h_tolerance),
                max(20, s_mean - s_tolerance),
                max(20, v_mean - v_tolerance)
            ])
            self.upper_color1 = np.array([
                min(180, h_mean + h_tolerance),
                255,
                255
            ])

    def process_frame(self, frame):
        h, w = frame.shape[:2]
        
        # Handle background capture
        if self.is_capturing_background:
            self.background_frames.append(frame.copy())
            self.background_capture_count += 1
            
            result = frame.copy()
            progress = (self.background_capture_count / self.background_capture_target) * 100
            
            # Semi-transparent background for progress UI
            overlay = result.copy()
            cv2.rectangle(overlay, (40, 40), (w-40, 160), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.75, result, 0.25, 0, result)
            
            # Progress text with outline
            draw_text_with_outline(result, f"Capturing Background: {int(progress)}%", (60, 80), 
                                  font_scale=0.9, text_color=(0, 255, 255))
            draw_text_with_outline(result, "Please stay out of frame!", (60, 120), 
                                  font_scale=0.6, text_color=(255, 255, 255))
            
            # Progress bar
            bar_x, bar_y = 60, 135
            bar_width = w - 120
            bar_height = 15
            fill_width = int(bar_width * (self.background_capture_count / self.background_capture_target))
            
            cv2.rectangle(result, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
            cv2.rectangle(result, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), (0, 255, 0), -1)
            cv2.rectangle(result, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 2)
            
            if self.background_capture_count >= self.background_capture_target:
                self.background = np.median(np.array(list(self.background_frames)), axis=0).astype(np.uint8)
                self.is_capturing_background = False
                self.background_capture_count = 0
                print("✓ Background captured and averaged!")
                
                if self.selected_color is None:
                    self.calibration_mode = True
                    print("➜ Auto-enabled calibration mode")
            
            return result

        if self.background is None:
            result = frame.copy()
            
            # Semi-transparent background for instructions
            overlay = result.copy()
            cv2.rectangle(overlay, (30, 50), (w-30, h-50), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.8, result, 0.2, 0, result)
            
            # Title
            draw_text_with_outline(result, "INVISIBILITY CLOAK - BEST MODE", (50, 100),
                                  font_scale=1.0, text_color=(0, 255, 255), thickness=2)
            
            # Step 1
            draw_text_with_outline(result, "STEP 1: Capture Background", (50, 160),
                                  font_scale=0.8, text_color=(0, 255, 255))
            draw_text_with_outline(result, "1. Clear the frame completely", (70, 195),
                                  font_scale=0.6, text_color=(255, 255, 255), thickness=1)
            draw_text_with_outline(result, "2. Ensure stable, bright lighting", (70, 225),
                                  font_scale=0.6, text_color=(255, 255, 255), thickness=1)
            draw_text_with_outline(result, "3. Press 'B' to capture 30 frames", (70, 255),
                                  font_scale=0.6, text_color=(255, 255, 255), thickness=1)
            
            # Step 2
            draw_text_with_outline(result, "STEP 2: Calibrate Cloak Color", (50, 310),
                                  font_scale=0.8, text_color=(150, 150, 150))
            draw_text_with_outline(result, "Click on your cloak after capture", (70, 345),
                                  font_scale=0.6, text_color=(200, 200, 200), thickness=1)
            
            # Tips
            cv2.line(result, (50, 375), (w-50, 375), (100, 100, 100), 1)
            draw_text_with_outline(result, "PRO TIP: Use solid red/green/blue cloth", (50, 410),
                                  font_scale=0.5, text_color=(255, 200, 100), thickness=1)
            
            return result

        # BEST QUALITY Invisibility Effect
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask
        if self.use_dual_range:
            mask1 = cv2.inRange(hsv, self.lower_color1, self.upper_color1)
            mask2 = cv2.inRange(hsv, self.lower_color2, self.upper_color2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv, self.lower_color1, self.upper_color1)

        # Enhanced morphological operations
        kernel = np.ones((self.morph_kernel_size, self.morph_kernel_size), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        # Temporal smoothing
        self.mask_history.append(mask)
        if len(self.mask_history) > 1:
            mask = np.mean(np.array(list(self.mask_history)), axis=0).astype(np.uint8)
        
        # Superior edge feathering
        mask = cv2.GaussianBlur(mask, (self.edge_blur_size, self.edge_blur_size), 0)
        
        # Normalize for alpha blending
        mask_float = mask.astype(float) / 255.0
        mask_float_3ch = np.stack([mask_float] * 3, axis=-1)
        
        # Alpha blending
        final_output = (frame * (1 - mask_float_3ch) + self.background * mask_float_3ch).astype(np.uint8)
        
        # Advanced boundary smoothing
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            boundary_mask = np.zeros_like(mask)
            cv2.drawContours(boundary_mask, contours, -1, 255, thickness=15)
            boundary_mask = cv2.GaussianBlur(boundary_mask, (21, 21), 0)
            
            blurred_output = cv2.GaussianBlur(final_output, (7, 7), 0)
            boundary_blend = boundary_mask.astype(float) / 255.0
            boundary_blend_3ch = np.stack([boundary_blend] * 3, axis=-1)
            final_output = (final_output * (1 - boundary_blend_3ch) + blurred_output * boundary_blend_3ch).astype(np.uint8)
        
        # Draw professional UI
        self._draw_ui(final_output, mask)
        
        return final_output
    
    def _draw_ui(self, frame, mask):
        """Draw professional UI with outlined text."""
        h, w = frame.shape[:2]
        
        # Top status bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 110), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        if self.calibration_mode:
            draw_text_with_outline(frame, "CALIBRATION MODE", (20, 40),
                                  font_scale=1.0, text_color=(0, 255, 255))
            draw_text_with_outline(frame, "Click on your cloak to calibrate color", (20, 75),
                                  font_scale=0.6, text_color=(255, 255, 255))
        elif self.selected_color is None:
            draw_text_with_outline(frame, "Press 'T' then click on your cloak", (20, 40),
                                  font_scale=1.0, text_color=(0, 255, 255))
            draw_text_with_outline(frame, "Calibration required for best results", (20, 75),
                                  font_scale=0.6, text_color=(255, 255, 255))
        else:
            draw_text_with_outline(frame, "INVISIBILITY ACTIVE", (20, 40),
                                  font_scale=1.0, text_color=(0, 255, 0))
            
            # Coverage and quality indicators
            coverage = (np.sum(mask > 128) / (h * w)) * 100
            draw_text_with_outline(frame, f"Cloak Coverage: {coverage:.1f}%", (20, 75),
                                  font_scale=0.6, text_color=(255, 255, 255))
            
            # Color swatch
            if self.selected_color is not None:
                color_bgr = tuple(map(int, self.selected_color))
                cv2.rectangle(frame, (w - 80, 20), (w - 20, 80), color_bgr, -1)
                cv2.rectangle(frame, (w - 80, 20), (w - 20, 80), (255, 255, 255), 3)
                draw_text_with_outline(frame, "Cloak", (w - 73, 100),
                                      font_scale=0.4, text_color=(255, 255, 255), thickness=1)
        
        # Bottom control bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, h-40), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        draw_text_with_outline(frame, "[B] Background  [T] Calibrate  [X] Reset  [+/-] Edge Blur", 
                              (20, h-15), font_scale=0.5, text_color=(255, 255, 255), thickness=1)

    def handle_input(self, key):
        if key == ord('b') or key == ord('B'):
            self.is_capturing_background = True
            self.background_capture_count = 0
            self.background_frames.clear()
            print("➜ Starting background capture (30 frames)...")
            
        elif key == ord('t') or key == ord('T'):
            self.calibration_mode = not self.calibration_mode
            if self.calibration_mode:
                print("➜ Calibration mode: CLICK on your cloak")
            else:
                print("✗ Calibration mode disabled")
                
        elif key == ord('x') or key == ord('X'):
            self.background = None
            self.background_frames.clear()
            self.selected_color = None
            self.mask_history.clear()
            print("➜ Reset complete.")
            
        elif key == ord('+') or key == ord('='):
            self.edge_blur_size = min(31, self.edge_blur_size + 2)
            if self.edge_blur_size % 2 == 0:
                self.edge_blur_size += 1
            print(f"Edge blur: {self.edge_blur_size}")
            
        elif key == ord('-') or key == ord('_'):
            self.edge_blur_size = max(3, self.edge_blur_size - 2)
            if self.edge_blur_size % 2 == 0:
                self.edge_blur_size -= 1
            print(f"Edge blur: {self.edge_blur_size}")
        
    def handle_mouse(self, event, x, y, frame):
        if event == cv2.EVENT_LBUTTONDOWN and self.calibration_mode:
            self.selected_point = (x, y)
            self.calibrate_from_click(frame, x, y)
            self.calibration_mode = False

    def get_name(self):
        return ""

    def get_controls(self):
        return [
            ("B", "Capture (30 frames)"),
            ("T", "Calibrate"),
            ("X", "Reset"),
            ("+/-", "Edge Blur")
        ]
