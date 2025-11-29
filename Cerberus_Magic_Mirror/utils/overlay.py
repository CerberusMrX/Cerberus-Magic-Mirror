import cv2
import config

class Overlay:
    @staticmethod
    def draw_text(frame, text, position, color=(255, 255, 255), scale=0.7, thickness=2, bg_color=None):
        """
        Draw text with an optional background and outline for better visibility.
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        x, y = position
        
        # Draw outline (black) for contrast
        cv2.putText(frame, text, position, font, scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
        
        # Draw main text
        cv2.putText(frame, text, position, font, scale, color, thickness, cv2.LINE_AA)

    @staticmethod
    def draw_status(frame, mode_name, controls):
        """
        Draw the status overlay including mode name and available controls.
        """
        h, w = frame.shape[:2]
        
        # 1. Draw Mode Name (Top Left)
        Overlay.draw_text(frame, mode_name, config.MODE_NAME_POSITION, 
                         color=config.MODE_NAME_COLOR, 
                         scale=config.MODE_NAME_SCALE, 
                         thickness=config.UI_FONT_THICKNESS)
        
        # 2. Draw Controls (Bottom Left)
        # We'll stack them from the bottom up
        bottom_margin = 20
        line_height = 25
        
        # Filter out empty controls
        active_controls = [c for c in controls if c]
        
        # Draw background for controls if there are any
        if active_controls:
            # Calculate box size
            max_width = 0
            total_height = len(active_controls) * line_height + 10
            
            for key, desc in active_controls:
                text = f"[{key}] {desc}"
                (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                max_width = max(max_width, text_w)
            
            # Draw semi-transparent background
            overlay = frame.copy()
            cv2.rectangle(overlay, (10, h - bottom_margin - total_height), (10 + max_width + 20, h - 10), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
            
            # Draw text
            y = h - bottom_margin
            for key, desc in reversed(active_controls):
                text = f"[{key}] {desc}"
                cv2.putText(frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
                y -= line_height
