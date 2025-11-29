from abc import ABC, abstractmethod

class BaseMode(ABC):
    @abstractmethod
    def process_frame(self, frame):
        """
        Process the input frame and return the result.
        """
        pass

    @abstractmethod
    def handle_input(self, key):
        """
        Handle mode-specific keyboard input.
        """
        pass

    @abstractmethod
    def get_name(self):
        """
        Return the display name of the mode.
        """
        pass

    @abstractmethod
    def get_controls(self):
        """
        Return a list of (key, description) tuples for the overlay.
        """
        pass
    
    def handle_mouse(self, event, x, y, frame):
        """
        Optional: Handle mouse events.
        Modes that need mouse interaction should override this method.
        """
        pass
