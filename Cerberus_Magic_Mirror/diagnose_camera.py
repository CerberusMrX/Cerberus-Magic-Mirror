import cv2

def test_camera(index):
    print(f"Testing camera index {index}...")
    # Try with V4L2 backend explicitly if possible, otherwise default
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
    if not cap.isOpened():
        print(f"  Failed to open camera index {index} with V4L2. Trying default...")
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            print(f"  Failed to open camera index {index}")
            return False

    # Try reading without setting any properties first
    ret, frame = cap.read()
    if ret:
        print(f"  SUCCESS: Captured frame from index {index} (Default settings)")
        print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
        return True
    else:
        print(f"  Failed to read frame from index {index} (Default settings)")
    
    # Try setting common resolutions
    resolutions = [(640, 480), (1280, 720), (320, 240)]
    for w, h in resolutions:
        print(f"  Testing resolution {w}x{h}...")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        ret, frame = cap.read()
        if ret:
            print(f"  SUCCESS: Captured frame from index {index} at {w}x{h}")
            cap.release()
            return True
        else:
            print(f"  Failed at {w}x{h}")

    cap.release()
    return False

print("Starting Camera Diagnosis...")
for i in range(4):
    if test_camera(i):
        print(f"\n✅ Camera found at index {i}")
        break
else:
    print("\n❌ No working camera found.")
