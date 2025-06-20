# modules/system_control.py
import os

def shutdown():
    os.system("shutdown now")

def restart():
    os.system("reboot")
