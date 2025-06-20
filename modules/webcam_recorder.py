# modules/webcam_recorder.py
import cv2, time, os

def record_webcam(duration=10, output_dir='videos'):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"cam_{int(time.time())}.avi")
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))
    start = time.time()
    while int(time.time() - start) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    cap.release()
    out.release()
    return filename
