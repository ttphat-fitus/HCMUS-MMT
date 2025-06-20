# modules/process_manager.py
import psutil, subprocess, os

def list_processes():
    return [p.name() for p in psutil.process_iter()]

def start_app(command):
    subprocess.Popen(command, shell=True)

def stop_app_by_name(name):
    for p in psutil.process_iter():
        if p.name() == name:
            p.terminate()
