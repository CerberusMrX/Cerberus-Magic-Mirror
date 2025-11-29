#!/usr/bin/env python3
"""Quick diagnostic to test modes"""
import cv2
import sys
sys.path.insert(0, '/home/cerberusmrxi/Desktop/New Folder/Cerberus_Magic_Mirror')

from modes.advanced_paint_mode import AdvancedPaintMode
from modes.cloak_mode import CloakMode

print("="*60)
print("MODE DIAGNOSTIC TEST")
print("="*60)

# Test Paint Mode
print("\n1. Testing Advanced Paint Mode...")
try:
    paint_mode = AdvancedPaintMode()
    print(f"   ✓ Paint mode created")
    print(f"   ✓ Name: {paint_mode.get_name()}")
    print(f"   ✓ Controls: {paint_mode.get_controls()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test Cloak Mode  
print("\n2. Testing Enhanced Cloak Mode...")
try:
    cloak_mode = CloakMode()
    print(f"   ✓ Cloak mode created")
    print(f"   ✓ Name: {cloak_mode.get_name()}")
    print(f"   ✓ Controls: {cloak_mode.get_controls()}")
    print(f"   ✓ Has handle_mouse: {hasattr(cloak_mode, 'handle_mouse')}")
    print(f"   ✓ Has capture_next_frame: {hasattr(cloak_mode, 'capture_next_frame')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n3. Testing main.py imports...")
try:
    from main import main
    print("   ✓ main.py imports successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
