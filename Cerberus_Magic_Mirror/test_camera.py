import cv2

def test_camera_with_settings(index, width, height, fps):
    print(f"Testing camera index {index} with {width}x{height} @ {fps}fps...")
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"  Failed to open camera index {index}")
        return False
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"  Set resolution: {actual_width}x{actual_height}")

    ret, frame = cap.read()
    if ret:
        print(f"  SUCCESS: Captured frame from index {index}")
        print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
        return True
    else:
        print(f"  Failed to read frame from index {index}")
        cap.release()
        return False

# Test with config values
test_camera_with_settings(0, 1280, 720, 30)
