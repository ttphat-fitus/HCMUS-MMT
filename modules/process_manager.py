#modules/process_manager.py
import subprocess
import psutil

def list_processes():
    return [(p.pid, p.name()) for p in psutil.process_iter()]

def start_app(app_command):
    try:
        subprocess.Popen(app_command, shell=True)
        return f"Opened: {app_command}"
    except Exception as e:
        return f"Unable to open: {e}"

def stop_process_by_name(name):
    stopped = 0
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == name:
            proc.kill()
            stopped += 1
    return f"Terminated {stopped} process {name}"