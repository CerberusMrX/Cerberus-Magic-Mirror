# Cerberus Magic Mirror - Video Recorder Utility
# Author: Sudeepa Wanigarathna

import cv2
import os
import time
from datetime import datetime
import config

class VideoRecorder:
    """Handles video recording functionality."""
    
    def __init__(self):
        self.is_recording = False
        self.video_writer = None
        self.output_filename = None
        self.start_time = None
        self.frame_count = 0
        
        # Ensure recording directory exists
        os.makedirs(config.RECORDING_DIR, exist_ok=True)
    
    def start_recording(self, frame_width, frame_height):
        """
        Start recording video.
        
        Args:
            frame_width: Width of frames to record
            frame_height: Height of frames to record
            
        Returns:
            bool: True if recording started successfully, False otherwise
        """
        if self.is_recording:
            print("Already recording!")
            return False
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_filename = os.path.join(
            config.RECORDING_DIR, 
            f"recording_{timestamp}.{config.RECORDING_FORMAT}"
        )
        
        # Define codec
        fourcc = cv2.VideoWriter_fourcc(*config.RECORDING_CODEC)
        
        # Create VideoWriter
        self.video_writer = cv2.VideoWriter(
            self.output_filename,
            fourcc,
            config.RECORDING_FPS,
            (frame_width, frame_height)
        )
        
        if not self.video_writer.isOpened():
            print("Error: Could not create video writer")
            self.video_writer = None
            return False
        
        self.is_recording = True
        self.start_time = time.time()
        self.frame_count = 0
        
        print(f"📹 Recording started: {self.output_filename}")
        return True
    
    def stop_recording(self):
        """
        Stop recording and save the video file.
        
        Returns:
            tuple: (success, filename, duration, frame_count)
        """
        if not self.is_recording:
            print("Not currently recording!")
            return False, None, 0, 0
        
        # Calculate duration
        duration = time.time() - self.start_time
        
        # Release video writer
        if self.video_writer:
            self.video_writer.release()
        
        self.is_recording = False
        filename = self.output_filename
        frame_count = self.frame_count
        
        # Reset state
        self.video_writer = None
        self.output_filename = None
        self.start_time = None
        self.frame_count = 0
        
        print(f"✅ Recording stopped: {filename}")
        print(f"   Duration: {duration:.1f}s, Frames: {frame_count}")
        
        return True, filename, duration, frame_count
    
    def write_frame(self, frame):
        """
        Write a frame to the video file.
        
        Args:
            frame: Frame to write (numpy array)
            
        Returns:
            bool: True if frame written successfully, False otherwise
        """
        if not self.is_recording or self.video_writer is None:
            return False
        
        self.video_writer.write(frame)
        self.frame_count += 1
        return True
    
    def get_recording_status(self):
        """
        Get current recording status.
        
        Returns:
            dict: Recording status information
        """
        if not self.is_recording:
            return {
                'is_recording': False,
                'filename': None,
                'duration': 0,
                'frame_count': 0
            }
        
        duration = time.time() - self.start_time
        return {
            'is_recording': True,
            'filename': self.output_filename,
            'duration': duration,
            'frame_count': self.frame_count
        }
    
    def cleanup(self):
        """Cleanup resources."""
        if self.is_recording:
            self.stop_recording()
