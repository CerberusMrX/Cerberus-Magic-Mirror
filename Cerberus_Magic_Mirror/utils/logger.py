# Cerberus Magic Mirror - Logger Utility
# Author: Sudeepa Wanigarathna

import logging
import os
from datetime import datetime
import config

class Logger:
    """Singleton logger for the application."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """Setup the logging configuration."""
        # Ensure log directory exists
        os.makedirs(config.LOG_DIR, exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger('CerberusMagicMirror')
        self._logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # Prevent duplicate logs
        if self._logger.handlers:
            return
        
        # File handler
        log_file = os.path.join(config.LOG_DIR, config.LOG_FILENAME)
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(config.LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
        
        # Log session start
        self._logger.info("=" * 60)
        self._logger.info(f"Cerberus Magic Mirror - Session Started")
        self._logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._logger.info("=" * 60)
    
    def debug(self, message):
        """Log debug message."""
        self._logger.debug(message)
    
    def info(self, message):
        """Log info message."""
        self._logger.info(message)
    
    def warning(self, message):
        """Log warning message."""
        self._logger.warning(message)
    
    def error(self, message):
        """Log error message."""
        self._logger.error(message)
    
    def critical(self, message):
        """Log critical message."""
        self._logger.critical(message)
    
    def log_mode_switch(self, mode_name):
        """Log mode switch."""
        self.info(f"Switched to mode: {mode_name}")
    
    def log_snapshot(self, filename):
        """Log snapshot capture."""
        self.info(f"Snapshot saved: {filename}")
    
    def log_recording_start(self, filename):
        """Log recording start."""
        self.info(f"Recording started: {filename}")
    
    def log_recording_stop(self, filename, duration, frames):
        """Log recording stop."""
        self.info(f"Recording stopped: {filename}")
        self.info(f"Duration: {duration:.1f}s, Frames: {frames}")
    
    def log_error(self, error_type, error_message):
        """Log error with details."""
        self.error(f"{error_type}: {error_message}")
    
    def log_session_end(self):
        """Log session end."""
        self.info("=" * 60)
        self.info("Cerberus Magic Mirror - Session Ended")
        self.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info("=" * 60)

# Global logger instance
logger = Logger()
