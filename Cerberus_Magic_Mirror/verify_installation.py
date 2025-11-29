import cv2
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from modes.cloak_mode import CloakMode
from modes.air_draw_mode import ARPaintMode
from modes.ghost_mode import GhostMode
from utils.overlay import Overlay

def test_modes():
    print("Testing modes...")
    
    # Create a dummy frame (720p)
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    # Add some color
    cv2.rectangle(frame, (100, 100), (200, 200), (0, 0, 255), -1) # Red box
    cv2.rectangle(frame, (300, 100), (400, 200), (255, 0, 0), -1) # Blue box

    # Test Cloak Mode
    print("Testing CloakMode...")
    cloak = CloakMode()
    # Simulate 'B' press
    cloak.handle_input(ord('b'))
    # Process frame (should capture background)
    res = cloak.process_frame(frame)
    assert res is not None
    assert res.shape == frame.shape
    print("CloakMode OK")

    # Test AR Paint Mode
    print("Testing ARPaintMode...")
    draw = ARPaintMode()
    # Process frame (should detect blue box and draw)
    res = draw.process_frame(frame)
    assert res is not None
    assert res.shape == frame.shape
    # Simulate 'C' press
    draw.handle_input(ord('c'))
    print("ARPaintMode OK")

    # Test Ghost Mode
    print("Testing GhostMode...")
    ghost = GhostMode()
    res = ghost.process_frame(frame)
    # Process another frame to test blending
    res = ghost.process_frame(frame)
    assert res is not None
    assert res.shape == frame.shape
    print("GhostMode OK")

    # Test Overlay
    print("Testing Overlay...")
    Overlay.draw_status(frame, "Test Mode", [("A", "Action")])
    print("Overlay OK")

    print("All tests passed!")

if __name__ == "__main__":
    test_modes()
