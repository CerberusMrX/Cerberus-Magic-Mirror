# Cerberus Magic Mirror - Main Application
# Author: Sudeepa Wanigarathna
# System: Kali Linux

import cv2
import time
import os
import sys
from modes.cloak_mode import CloakMode
from modes.air_draw_mode import ARPaintMode
from modes.ghost_mode import GhostMode
from utils.overlay import Overlay
from utils.recorder import VideoRecorder
from utils.logger import logger
import config

def main():
    """Main application loop."""
    
    logger.info("Starting Cerberus Magic Mirror")
    
    # Ensure output directories exist
    os.makedirs(config.SNAPSHOT_DIR, exist_ok=True)
    os.makedirs(config.RECORDING_DIR, exist_ok=True)
    os.makedirs(config.LOG_DIR, exist_ok=True)
    
    # Initialize Webcam
    logger.info(f"Initializing webcam (device {config.CAMERA_INDEX})")
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    
    if not cap.isOpened():
        error_msg = "Could not open webcam. Please ensure a webcam is connected and accessible."
        logger.error(error_msg)
        print(f"\n❌ ERROR: {error_msg}")
        print("\nTroubleshooting:")
        print("1. Check if webcam is connected: ls /dev/video*")
        print("2. Check permissions: sudo usermod -aG video $USER")
        print("3. Try different camera index in config.py")
        sys.exit(1)

    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
    
    # Get actual resolution
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    logger.info(f"Camera resolution: {actual_width}x{actual_height}")

    # Initialize Modes (Only 3 Essential Modes)
    modes = {
        ord('1'): CloakMode(),
        ord('2'): ARPaintMode(),
        ord('3'): GhostMode(),
    }
    
    # Default Mode
    current_mode = modes[ord('1')]
    logger.log_mode_switch(current_mode.get_name())
    
    # Initialize Video Recorder
    recorder = VideoRecorder()
    
    # State variables
    paused = False
    show_help = False
    fps_counter = 0
    fps_start_time = time.time()
    current_fps = 0
    
    # Mouse callback state
    mouse_frame = None
    
    def mouse_callback(event, x, y, flags, param):
        """Global mouse callback for all modes."""
        nonlocal mouse_frame
        if mouse_frame is not None and hasattr(current_mode, 'handle_mouse'):
            current_mode.handle_mouse(event, x, y, mouse_frame)
    
    # Set mouse callback
    cv2.namedWindow(config.WINDOW_NAME)
    cv2.setMouseCallback(config.WINDOW_NAME, mouse_callback)
    
    # Welcome message
    print("\n" + "="*60)
    print("🎭 CERBERUS MAGIC MIRROR 🎭")
    print("="*60)
    print("Author: Sudeepa Wanigarathna")
    print("System: Kali Linux")
    print("\nModes:")
    print("  [1] Invisibility Cloak (Best)")
    print("  [2] AR Paint Mode (Full AR)")
    print("  [3] Ghost Trail")
    print("\nControls:")
    print("  [S] Snapshot  [R] Record  [H] Help  [P] Pause  [Q] Quit")
    print("="*60)
    print("\n✅ Application started successfully!\n")

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                error_msg = "Failed to capture frame"
                logger.error(error_msg)
                print(f"\n❌ ERROR: {error_msg}")
                break

            # Flip frame for mirror effect
            if config.MIRROR_EFFECT:
                frame = cv2.flip(frame, 1)
            
            # Store frame for mouse callback
            mouse_frame = frame.copy()

        # Handle Input
        key = cv2.waitKey(config.WAITKEY_DELAY) & 0xFF

        # Global controls
        if key == ord('q') or key == ord('Q'):
            logger.info("Quit requested by user")
            break
            
        elif key == ord('h') or key == ord('H'):
            show_help = not show_help
            logger.debug(f"Help toggled: {show_help}")
            
        elif key == ord('p') or key == ord('P'):
            paused = not paused
            logger.debug(f"Pause toggled: {paused}")
            print(f"{'⏸️  Paused' if paused else '▶️  Resumed'}")
            continue
            
        elif key == ord('s') or key == ord('S'):
            # Save Snapshot
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = os.path.join(config.SNAPSHOT_DIR, f"snapshot_{timestamp}.{config.SNAPSHOT_FORMAT}")
            
            if config.SNAPSHOT_FORMAT.lower() == 'jpg':
                cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, config.SNAPSHOT_QUALITY])
            else:
                cv2.imwrite(filename, frame)
            
            logger.log_snapshot(filename)
            print(f"📸 Snapshot saved: {filename}")
            
            # Show brief confirmation
            temp_frame = frame.copy()
            Overlay.draw_text(temp_frame, "Snapshot Saved!", (50, 50), color=(0, 255, 0), scale=1.5, thickness=3)
            cv2.imshow(config.WINDOW_NAME, temp_frame)
            cv2.waitKey(300)
            continue
            
        elif key == ord('r') or key == ord('R'):
            # Toggle recording (but not if in ghost mode where R is reset)
            if isinstance(current_mode, GhostMode):
                # Let ghost mode handle this
                current_mode.handle_input(key)
            else:
                if not recorder.is_recording:
                    if recorder.start_recording(actual_width, actual_height):
                        logger.log_recording_start(recorder.output_filename)
                else:
                    success, filename, duration, frames = recorder.stop_recording()
                    if success:
                        logger.log_recording_stop(filename, duration, frames)
                        print(f"💾 Recording saved: {filename}")
            
        elif key in modes:
            # Switch mode
            current_mode = modes[key]
            logger.log_mode_switch(current_mode.get_name())
            print(f"✨ Switched to: {current_mode.get_name()}")
            
        elif key != 255:  # 255 means no key pressed
            # Pass other keys to current mode
            current_mode.handle_input(key)

        if paused:
            # Show paused indicator
            display_frame = frame.copy()
            h, w = display_frame.shape[:2]
            cv2.rectangle(display_frame, (0, 0), (w, h), (0, 0, 0), -1)
            cv2.putText(display_frame, "PAUSED", (w//2 - 100, h//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
            cv2.putText(display_frame, "Press P to resume", (w//2 - 150, h//2 + 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow(config.WINDOW_NAME, display_frame)
            continue

        # Process Frame
        processed_frame = current_mode.process_frame(frame)

        # Calculate FPS
        fps_counter += 1
        if time.time() - fps_start_time >= 1.0:
            current_fps = fps_counter
            fps_counter = 0
            fps_start_time = time.time()

        # Draw Overlays
        if current_mode.get_name():
            Overlay.draw_status(processed_frame, current_mode.get_name(), current_mode.get_controls())
        
        # Draw recording indicator
        if recorder.is_recording:
            h, w = processed_frame.shape[:2]
            cv2.circle(processed_frame, (w - 30, 30), config.RECORDING_INDICATOR_SIZE, 
                      config.RECORDING_INDICATOR_COLOR, -1)
            status = recorder.get_recording_status()
            rec_text = f"REC {status['duration']:.0f}s"
            cv2.putText(processed_frame, rec_text, (w - 120, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw FPS counter
        if config.SHOW_FPS:
            Overlay.draw_text(processed_frame, f"FPS: {current_fps}", 
                            config.FPS_POSITION, color=config.FPS_COLOR)
        
        # Draw help overlay
        if show_help:
            h, w = processed_frame.shape[:2]
            overlay = processed_frame.copy()
            cv2.rectangle(overlay, (50, 50), (w - 50, h - 50), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, processed_frame, 0.3, 0, processed_frame)
            
            y_offset = 80
            for line in config.HELP_TEXT:
                cv2.putText(processed_frame, line, (70, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 25

        # Write frame to recording if active
        if recorder.is_recording:
            recorder.write_frame(processed_frame)

        # Show Frame
        cv2.imshow(config.WINDOW_NAME, processed_frame)

    # Cleanup
    logger.info("Cleaning up resources")
    recorder.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    logger.log_session_end()
    print("\n👋 Cerberus Magic Mirror Closed. Goodbye!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ ERROR: {str(e)}")
        print("Check logs/cerberus_magic_mirror.log for details")
        sys.exit(1)
