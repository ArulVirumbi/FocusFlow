import json
import time
import threading
from datetime import datetime
from win10toast import ToastNotifier
import pystray
from pystray import MenuItem as item
from PIL import Image
# import ctypes
import sys
import os
import tkinter as tk

# Suppress specific TypeError from WNDPROC
_original_excepthook = sys.excepthook

def _suppress_wndproc_errors(exc_type, exc_value, exc_traceback):
    if exc_type == TypeError and 'WPARAM is simple' in str(exc_value):
        return  # ignore
    _original_excepthook(exc_type, exc_value, exc_traceback)

sys.excepthook = _suppress_wndproc_errors
sys.stderr = open(os.devnull, 'w')  # Suppress WNDPROC error output

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

WORK_DURATION = config.get('work_duration_min', 25) * 60  # seconds
REST_DURATION = config.get('rest_duration_min', 5) * 60
TIME_BLOCKS = [(block['start'], block['end']) for block in config.get('time_blocks', [])]

# Initialize notifier and state
notifier = ToastNotifier()
running = True

MB_ICONINFORMATION = 0x40
MB_OK = 0x0


# def show_popup(title, message, timeout=5):
#     # Timeout in milliseconds
#     ctypes.windll.user32.MessageBoxTimeoutW(
#         0,
#         message,
#         title,
#         MB_ICONINFORMATION,
#         0,
#         timeout * 1000
#     )


def show_popup(title, message, timeout=5000):
    def close_popup():
        root.destroy()

    root = tk.Tk()
    root.title(title)
    root.attributes('-topmost', True)
    root.geometry("300x150")  # Box size

    # Remove default decorations
    root.overrideredirect(True)

    # Add padding and styling
    frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    frame.pack(expand=True, fill='both')

    label = tk.Label(
        frame, text=message, font=("Segoe UI", 20), wraplength=260, justify="center", bg="#f0f0f0"
    )
    label.pack(expand=True)

    # Position window near bottom right
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - 320
    y = screen_height - 180
    root.geometry(f"300x150+{x}+{y}")

    root.after(timeout, close_popup)
    root.mainloop()



def in_time_block():
    now = datetime.now().time()
    for start_str, end_str in TIME_BLOCKS:
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
        if start_time <= now <= end_time:
            return True
    return False


# def notify(title, msg):    #Variation: for using with ctypes
#     notifier.show_toast(title, msg, duration=5, threaded=True)
#     show_popup(title, msg, timeout=5)

def notify(title, msg):
    notifier.show_toast(title, msg, duration=5, threaded=True)
    threading.Thread(target=show_popup, args=(title, msg), daemon=True).start()


def countdown(seconds):
    start = time.time()
    while running and time.time() - start < seconds:
        time.sleep(1)


def timer_loop():
    global running
    while running:
        if in_time_block():
            notify("🧠 Work Time Started", "Focus now!")
            countdown(WORK_DURATION)
            if not running:
                break
            notify("☕ Break Time", "Relax for 5 minutes")
            countdown(REST_DURATION)
        else:
            time.sleep(30)


def quit_app(icon, item):
    global running
    running = False
    icon.stop()
    return 0  # ensure valid WNDPROC return


def setup_tray():
    icon = pystray.Icon("FocusFlow")
    icon.icon = Image.new('RGB', (64, 64), color=(255, 255, 255))
    icon.menu = pystray.Menu(item('Quit', quit_app))
    threading.Thread(target=timer_loop, daemon=True).start()
    try:
        icon.run()
    except TypeError as e:
        if 'WPARAM is simple' in str(e):
            pass
        else:
            raise


if __name__ == '__main__':
    threading.Thread(target=setup_tray, daemon=True).start()
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass