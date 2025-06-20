import cv2
import os
import time

def record_webcam(duration=5, output_dir='videos'):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"test_{int(time.time())}.avi")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Không mở được webcam. Kiểm tra thiết bị hoặc quyền.")
        return None

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    print(f"▶️ Đang quay video trong {duration} giây...")

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            print("⚠️ Không nhận được frame từ webcam.")
            break

    cap.release()
    out.release()
    print(f"✅ Video đã lưu tại: {filename}")
    return filename

record_webcam()
