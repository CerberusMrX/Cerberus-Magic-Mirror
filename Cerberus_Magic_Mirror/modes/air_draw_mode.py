import cv2
import numpy as np
from collections import deque
from .base_mode import BaseMode
import config
import time
import math

# Try to import MediaPipe
try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False
    print("⚠️ MediaPipe not found. Finger tracking will use legacy color mode.")

class ARPaintMode(BaseMode):
    def __init__(self):
        # Tracking colors
        self.lower_blue = np.array(config.DRAW_LOWER_BLUE)
        self.upper_blue = np.array(config.DRAW_UPPER_BLUE)
        
        self.tracking_mode = 'object'  # Default to object mode for better compatibility
        self.canvas = None
        self.points = deque(maxlen=config.DRAW_MAX_POINTS)
        
        # MediaPipe Setup
        if HAS_MEDIAPIPE:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7,
                max_num_hands=1
            )
            self.mp_draw = mp.solutions.drawing_utils
        
        # Paint settings
        self.colors = config.PAINT_COLORS
        self.drawing_color = self.colors[5]
        self.current_brush_size = config.PAINT_BRUSH_SIZES[2]
        self.is_eraser = False
        
        # UI Settings
        self.toolbar_height = 120
        self.selected_color_idx = 5
        self.selected_brush_idx = 2
        
        # Interaction
        self.hover_element = None
        self.hover_start_time = 0
        self.dwell_time = 0.7
        
        # Gesture tracking
        self.gesture_mode = 'hover'
        
        # Calibration
        self.calibration_mode = False
        self.calibrated_color = None
        
    def calibrate_from_click(self, frame, x, y):
        """Calibrate tracking color from clicked point."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Sample region
        sample_size = 10
        x1, y1 = max(0, x-sample_size), max(0, y-sample_size)
        x2, y2 = min(frame.shape[1], x+sample_size), min(frame.shape[0], y+sample_size)
        region = hsv[y1:y2, x1:x2]
        
        # Calculate mean and std
        h_mean = np.mean(region[:,:,0])
        s_mean = np.mean(region[:,:,1])
        v_mean = np.mean(region[:,:,2])
        
        std_dev = np.std(region[:,:,0])
        tolerance = max(20, int(std_dev * 3))
        
        # Set new bounds
        self.lower_blue = np.array([max(0, h_mean - tolerance), max(50, s_mean - 50), max(50, v_mean - 50)])
        self.upper_blue = np.array([min(180, h_mean + tolerance), 255, 255])
        
        self.calibrated_color = (int(h_mean), int(s_mean), int(v_mean))
        print(f"✓ Calibrated to HSV: {self.calibrated_color}")
        
    def _calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two points."""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def _get_fingertip_mediapipe(self, frame):
        """Get fingertip position and detect pinch gesture."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            
            # Get landmarks
            index_tip = (int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h))
            thumb_tip = (int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h))
            middle_tip = (int(hand_landmarks.landmark[12].x * w), int(hand_landmarks.landmark[12].y * h))
            
            # Calculate distances
            pinch_dist = self._calculate_distance(index_tip, thumb_tip)
            erase_dist = self._calculate_distance(index_tip, middle_tip)
            
            # Determine gesture
            gesture = 'hover'
            PINCH_THRESHOLD = 40
            ERASE_THRESHOLD = 45
            
            if erase_dist < ERASE_THRESHOLD:
                gesture = 'erase'
            elif pinch_dist < PINCH_THRESHOLD:
                gesture = 'draw'
            
            return index_tip, gesture, hand_landmarks
            
        return None, 'hover', None

    def _draw_text(self, frame, text, pos, scale=0.6, color=(255, 255, 255), thickness=2):
        """Draw text with outline."""
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Outline
        cv2.putText(frame, text, pos, font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
        # Text
        cv2.putText(frame, text, pos, font, scale, color, thickness, cv2.LINE_AA)

    def _check_ui_click(self, x, y, h, w):
        """Check if position clicks any UI element."""
        toolbar_y = h - self.toolbar_height
        
        if y < toolbar_y - 50:
            return None
        
        # Mode Switch Button (Top Right - Large)
        mode_btn = {
            'x1': w - 200,
            'y1': toolbar_y - 45,
            'x2': w - 20,
            'y2': toolbar_y - 10
        }
        if mode_btn['x1'] <= x <= mode_btn['x2'] and mode_btn['y1'] <= y <= mode_btn['y2']:
            return {'type': 'mode_switch', 'rect': mode_btn}
        
        # Clear Button (Left side)
        clear_btn = {
            'x1': 10,
            'y1': toolbar_y + 20,
            'x2': 80,
            'y2': toolbar_y + 70
        }
        if clear_btn['x1'] <= x <= clear_btn['x2'] and clear_btn['y1'] <= y <= clear_btn['y2']:
            return {'type': 'clear', 'rect': clear_btn}
            
        # Save Button (Next to Clear)
        save_btn = {
            'x1': 90,
            'y1': toolbar_y + 20,
            'x2': 160,
            'y2': toolbar_y + 70
        }
        if save_btn['x1'] <= x <= save_btn['x2'] and save_btn['y1'] <= y <= save_btn['y2']:
            return {'type': 'save', 'rect': save_btn}
        
        # Color Palette (Center - 2 Rows)
        color_start_x = 180
        color_start_y = toolbar_y + 15
        color_size = 30
        color_spacing = 5
        colors_per_row = 6
        
        for i in range(len(self.colors)):
            row = i // colors_per_row
            col = i % colors_per_row
            
            cx = color_start_x + col * (color_size + color_spacing)
            cy = color_start_y + row * (color_size + color_spacing)
            
            if cx <= x <= cx + color_size and cy <= y <= cy + color_size:
                return {'type': 'color', 'value': i, 'rect': {'x1': cx, 'y1': cy, 'x2': cx + color_size, 'y2': cy + color_size}}
        
        # Eraser Button
        eraser_x = 410
        eraser_y = toolbar_y + 20
        if eraser_x <= x <= eraser_x + 50 and eraser_y <= y <= eraser_y + 50:
             return {'type': 'eraser', 'rect': {'x1': eraser_x, 'y1': eraser_y, 'x2': eraser_x + 50, 'y2': eraser_y + 50}}

        # Brush Sizes (Right)
        brush_start_x = 480
        brush_y = toolbar_y + 25
        
        for i in range(len(config.PAINT_BRUSH_SIZES)):
            bx = brush_start_x + i * 35
            if bx <= x <= bx + 30 and brush_y <= y <= brush_y + 30:
                return {'type': 'brush', 'value': i, 'rect': {'x1': bx, 'y1': brush_y, 'x2': bx + 30, 'y2': brush_y + 30}}
        
        return None

    def _handle_element_click(self, element):
        """Handle UI element clicks."""
        if element['type'] == 'mode_switch':
            if HAS_MEDIAPIPE:
                try:
                    # Test if MediaPipe actually works
                    if not hasattr(self, 'hands') or self.hands is None:
                        print("⚠️ MediaPipe installed but not functional. Staying in object mode.")
                        return
                    self.tracking_mode = 'object' if self.tracking_mode == 'finger' else 'finger'
                    print(f"🔄 Switched to {self.tracking_mode.upper()} tracking")
                except Exception as e:
                    print(f"⚠️ Cannot switch to finger mode: {e}")
            else:
                print("⚠️ MediaPipe not available. Install it to use finger tracking.")
        
        elif element['type'] == 'clear':
            self.canvas = None
            self.points.clear()
            print("🗑️ Canvas cleared")
            
        elif element['type'] == 'save':
            self._save_canvas()
            
        elif element['type'] == 'eraser':
            self.is_eraser = True
            print("🧹 Eraser selected")
        
        elif element['type'] == 'color':
            self.selected_color_idx = element['value']
            self.drawing_color = self.colors[element['value']]
            self.is_eraser = False
            print(f"🎨 Color {element['value'] + 1}")
        
        elif element['type'] == 'brush':
            self.selected_brush_idx = element['value']
            self.current_brush_size = config.PAINT_BRUSH_SIZES[element['value']]
            # Don't disable eraser if just changing size, unless we want to? 
            # Usually changing brush size keeps current tool. 
            # But here brushes are distinct from eraser. Let's keep eraser active if it was active?
            # Actually, usually clicking a brush size implies using the brush.
            # But let's say if we are in eraser mode, clicking size changes eraser size?
            # For simplicity, let's say clicking brush size switches to brush.
            self.is_eraser = False 
            print(f"🖌️ Brush size: {self.current_brush_size}px")

    def _save_canvas(self):
        """Save the current canvas."""
        if self.canvas is not None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{config.SNAPSHOT_DIR}/painting_{timestamp}.png"
            # We need to save the combined result, not just the black canvas
            # But usually people want the art. The canvas is black background with colored lines.
            # Let's save the canvas itself.
            cv2.imwrite(filename, self.canvas)
            print(f"💾 Painting saved: {filename}")
        else:
            print("⚠️ Canvas is empty!")

    def process_frame(self, frame):
        h, w = frame.shape[:2]
        
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

        center = None
        hand_landmarks = None
        toolbar_y = h - self.toolbar_height

        # --- TRACKING ---
        if self.tracking_mode == 'finger' and HAS_MEDIAPIPE:
            center, self.gesture_mode, hand_landmarks = self._get_fingertip_mediapipe(frame)
            
            if self.gesture_mode == 'erase':
                self.is_eraser = True
            elif self.gesture_mode == 'draw':
                self.is_eraser = False
        else:
            # Object tracking
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
            mask = cv2.GaussianBlur(mask, (7, 7), 0)
            
            cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if M["m00"] > 0 and radius > config.DRAW_MIN_RADIUS:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    self.gesture_mode = 'draw'
            
            if not center:
                self.gesture_mode = 'hover'

        # --- DRAWING & INTERACTION ---
        hover_progress = 0
        
        # Handle calibration click
        if self.calibration_mode:
             # Just show cursor, click handled in handle_mouse (not implemented in base yet, so we use logic here)
             # Actually BaseMode doesn't have handle_mouse, main.py calls it.
             # We need to implement handle_mouse in this class.
             pass
        
        if center:
            cx, cy = center
            
            # Cursor visualization
            cursor_color = (0, 255, 0) if self.gesture_mode == 'draw' else (0, 100, 255) if self.gesture_mode == 'erase' else (200, 200, 200)
            cursor_radius = 12 if self.gesture_mode == 'draw' else 16
            
            cv2.circle(frame, (cx, cy), cursor_radius, cursor_color, -1)
            cv2.circle(frame, (cx, cy), cursor_radius + 3, (255, 255, 255), 2)
            
            # Draw hand skeleton
            if hand_landmarks and HAS_MEDIAPIPE:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # UI Interaction
            if cy >= toolbar_y - 50:
                self.points.clear()
                
                element = self._check_ui_click(cx, cy, h, w)
                if element:
                    if self.hover_element and self.hover_element['type'] == element['type']:
                        if element['type'] in ['color', 'brush'] and self.hover_element.get('value') != element.get('value'):
                            self.hover_element = element
                            self.hover_start_time = time.time()
                        else:
                            elapsed = time.time() - self.hover_start_time
                            hover_progress = min(elapsed / self.dwell_time, 1.0)
                            
                            if elapsed >= self.dwell_time:
                                self._handle_element_click(element)
                                self.hover_start_time = time.time()
                                hover_progress = 0
                    else:
                        self.hover_element = element
                        self.hover_start_time = time.time()
                else:
                    self.hover_element = None
            else:
                # Drawing area
                self.hover_element = None
                
                if self.gesture_mode in ['draw', 'erase']:
                    self.points.appendleft(center)
                else:
                    if len(self.points) > 0 and self.points[0] is not None:
                        self.points.appendleft(None)
        else:
            if len(self.points) > 0 and self.points[0] is not None:
                self.points.appendleft(None)
            self.hover_element = None

        # Render drawing
        if len(self.points) >= 2:
            for i in range(1, len(self.points)):
                if self.points[i-1] is None or self.points[i] is None:
                    continue
                
                if self.points[i-1][1] < toolbar_y and self.points[i][1] < toolbar_y:
                    color = (0, 0, 0) if self.is_eraser else self.drawing_color
                    thickness = 30 if self.is_eraser else self.current_brush_size
                    cv2.line(self.canvas, self.points[i], self.points[i-1], color, thickness, cv2.LINE_AA)
        
        # Combine canvas and frame
        gray_canvas = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, canvas_mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)
        canvas_inv = cv2.bitwise_not(canvas_mask)
        
        frame_bg = cv2.bitwise_and(frame, frame, mask=canvas_inv)
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=canvas_mask)
        result = cv2.add(frame_bg, canvas_fg)
        
        # Draw UI
        self._draw_ui(result, h, w, hover_progress)
        
        return result

    def _draw_ui(self, frame, h, w, hover_progress):
        """Draw clean professional UI."""
        toolbar_y = h - self.toolbar_height
        
        # === TOP STATUS BAR ===
        status_bar_h = 40
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, status_bar_h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
        cv2.line(frame, (0, status_bar_h), (w, status_bar_h), (0, 200, 255), 2)
        
        # Tracking mode indicator
        mode_text = f"TRACKING: {self.tracking_mode.upper()}"
        mode_color = (0, 255, 255) if self.tracking_mode == 'finger' else (255, 150, 0)
        self._draw_text(frame, mode_text, (20, 27), 0.7, mode_color, 2)
        
        # Gesture status
        if self.tracking_mode == 'finger':
            gesture_text = f"GESTURE: {self.gesture_mode.upper()}"
            g_color = (0, 255, 0) if self.gesture_mode == 'draw' else (0, 100, 255) if self.gesture_mode == 'erase' else (200, 200, 200)
            text_w = cv2.getTextSize(gesture_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0][0]
            self._draw_text(frame, gesture_text, (w//2 - text_w//2, 27), 0.7, g_color, 2)
        
        # Help text
        if self.calibration_mode:
            help_text = "CLICK ON OBJECT TO CALIBRATE"
            help_color = (0, 255, 255)
        else:
            help_text = "Pinch=Draw | 2Fingers=Erase" if self.tracking_mode == 'finger' else "Press 'T' to Calibrate Object"
            help_color = (180, 180, 180)
            
        self._draw_text(frame, help_text, (w - 450, 27), 0.5, help_color, 1)
        
        # === MODE SWITCH BUTTON (Large, Right Side) ===
        mode_btn_x1 = w - 200
        mode_btn_y1 = toolbar_y - 45
        mode_btn_x2 = w - 20
        mode_btn_y2 = toolbar_y - 10
        
        btn_color = (0, 200, 255) if self.tracking_mode == 'finger' else (255, 150, 0)
        btn_text = "🖐 FINGER MODE" if self.tracking_mode == 'finger' else "🔵 OBJECT MODE"
        
        cv2.rectangle(frame, (mode_btn_x1, mode_btn_y1), (mode_btn_x2, mode_btn_y2), btn_color, -1)
        cv2.rectangle(frame, (mode_btn_x1, mode_btn_y1), (mode_btn_x2, mode_btn_y2), (255, 255, 255), 2)
        
        text_size = cv2.getTextSize(btn_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = mode_btn_x1 + (mode_btn_x2 - mode_btn_x1 - text_size[0]) // 2
        text_y = mode_btn_y1 + (mode_btn_y2 - mode_btn_y1 + text_size[1]) // 2
        self._draw_text(frame, btn_text, (text_x, text_y), 0.6, (255, 255, 255), 2)
        
        # === BOTTOM TOOLBAR ===
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, toolbar_y), (w, h), (25, 25, 25), -1)
        cv2.addWeighted(overlay, 0.92, frame, 0.08, 0, frame)
        cv2.line(frame, (0, toolbar_y), (w, toolbar_y), (0, 200, 255), 3)
        
        # Section 1: Clear & Save
        # Clear
        cv2.rectangle(frame, (10, toolbar_y + 20), (80, toolbar_y + 70), (50, 50, 200), -1)
        cv2.rectangle(frame, (10, toolbar_y + 20), (80, toolbar_y + 70), (255, 255, 255), 2)
        self._draw_text(frame, "CLR", (20, toolbar_y + 53), 0.6, (255, 255, 255), 2)
        
        # Save
        cv2.rectangle(frame, (90, toolbar_y + 20), (160, toolbar_y + 70), (50, 200, 50), -1)
        cv2.rectangle(frame, (90, toolbar_y + 20), (160, toolbar_y + 70), (255, 255, 255), 2)
        self._draw_text(frame, "SAVE", (100, toolbar_y + 53), 0.6, (255, 255, 255), 2)
        
        # Section 2: Color Palette (2 Rows)
        self._draw_text(frame, "COLORS", (180, toolbar_y + 12), 0.4, (150, 150, 150), 1)
        
        color_start_x = 180
        color_start_y = toolbar_y + 15
        color_size = 30
        color_spacing = 5
        colors_per_row = 6
        
        for i, color in enumerate(self.colors):
            row = i // colors_per_row
            col = i % colors_per_row
            
            cx = color_start_x + col * (color_size + color_spacing)
            cy = color_start_y + row * (color_size + color_spacing)
            
            # Highlight selected
            if i == self.selected_color_idx and not self.is_eraser:
                cv2.rectangle(frame, (cx - 2, cy - 2), (cx + color_size + 2, cy + color_size + 2), (255, 255, 255), 2)
            
            cv2.rectangle(frame, (cx, cy), (cx + color_size, cy + color_size), color, -1)
            cv2.rectangle(frame, (cx, cy), (cx + color_size, cy + color_size), (100, 100, 100), 1)
            
        # Section 3: Eraser
        eraser_x = 410
        eraser_y = toolbar_y + 20
        eraser_color = (200, 200, 200) if self.is_eraser else (50, 50, 50)
        text_color = (0, 0, 0) if self.is_eraser else (255, 255, 255)
        
        cv2.rectangle(frame, (eraser_x, eraser_y), (eraser_x + 50, eraser_y + 50), eraser_color, -1)
        cv2.rectangle(frame, (eraser_x, eraser_y), (eraser_x + 50, eraser_y + 50), (255, 255, 255), 2)
        self._draw_text(frame, "ERASE", (eraser_x + 2, eraser_y + 30), 0.4, text_color, 1)

        # Section 4: Brush Sizes
        self._draw_text(frame, "SIZE", (480, toolbar_y + 12), 0.4, (150, 150, 150), 1)
        
        brush_start_x = 480
        brush_y = toolbar_y + 25
        
        for i, brush_size in enumerate(config.PAINT_BRUSH_SIZES):
            bx = brush_start_x + i * 35
            
            is_selected = (i == self.selected_brush_idx)
            border_color = (0, 255, 0) if is_selected else (100, 100, 100)
            
            cv2.rectangle(frame, (bx, brush_y), (bx + 30, brush_y + 30), (40, 40, 40), -1)
            cv2.rectangle(frame, (bx, brush_y), (bx + 30, brush_y + 30), border_color, 2)
            cv2.circle(frame, (bx + 15, brush_y + 15), min(brush_size // 2, 12), (255, 255, 255), -1)
        
        # Hover progress indicator
        if self.hover_element and hover_progress > 0:
            rect = self.hover_element['rect']
            if isinstance(rect, dict):
                cx = (rect['x1'] + rect['x2']) // 2
                cy = (rect['y1'] + rect['y2']) // 2
            else:
                cx = (rect[0] + rect[2]) // 2
                cy = (rect[1] + rect[3]) // 2
            
            cv2.ellipse(frame, (cx, cy), (22, 22), 0, 0, int(360 * hover_progress), (0, 255, 0), 4)

    def handle_input(self, key):
        if key == ord('c') or key == ord('C'):
            self.canvas = None
            self.points.clear()
        elif key == ord('f') or key == ord('F'):
            if HAS_MEDIAPIPE:
                self.tracking_mode = 'object' if self.tracking_mode == 'finger' else 'finger'
        elif key == ord('t') or key == ord('T'):
            self.calibration_mode = not self.calibration_mode
            print(f"Calibration Mode: {self.calibration_mode}")

    def handle_mouse(self, event, x, y, frame):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.calibration_mode:
                self.calibrate_from_click(frame, x, y)
                self.calibration_mode = False

    def get_name(self):
        return ""

    def get_controls(self):
        return []
