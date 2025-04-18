import json
import time
import threading
from datetime import datetime
from win10toast import ToastNotifier
import pystray
from pystray import MenuItem as item
from PIL import Image
import ctypes
import sys
import tkinter as tk

# Suppress specific TypeError from WNDPROC
_original_excepthook = sys.excepthook

def _suppress_wndproc_errors(exc_type, exc_value, exc_traceback):
    if exc_type == TypeError and 'WPARAM is simple' in str(exc_value):
        return  # ignore
    _original_excepthook(exc_type, exc_value, exc_traceback)

sys.excepthook = _suppress_wndproc_errors

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

WORK_DURATION = config.get('work_duration_min', 25) * 60  # seconds
REST_DURATION = config.get('rest_duration_min', 5) * 60
TIME_BLOCKS = [(block['start'], block['end']) for block in config.get('time_blocks', [])]

# Initialize notifier and state
notifier = ToastNotifier()
running = True

# Win32 MessageBoxTimeout fallback
MB_OK = 0x00000000
MSGBUTTON = MB_OK
MSGTIMEOUT = 5000  # milliseconds

def show_win_msgbox(title, message):
    try:
        ctypes.windll.user32.MessageBoxTimeoutW(0, message, title, MSGBUTTON, 0, MSGTIMEOUT)
    except Exception:
        pass

def show_popup(title, message):
    def close():
        popup.destroy()

    popup = tk.Tk()
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.configure(bg="white")

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    width, height = 300, 150
    x = screen_width - width - 20
    y = screen_height - height - 100
    popup.geometry(f"{width}x{height}+{x}+{y}")

    frame = tk.Frame(popup, bg="white", padx=20, pady=20)
    frame.pack(expand=True, fill='both')

    label_title = tk.Label(frame, text=title, font=("Segoe UI", 20, "bold"), bg="white")
    label_title.pack(pady=(0, 10))

    label_msg = tk.Label(frame, text=message, font=("Segoe UI", 18), bg="white", wraplength=260, justify="center")
    label_msg.pack()

    popup.after(MSGTIMEOUT, close)
    popup.mainloop()

def in_time_block():
    now = datetime.now().time()
    for start_str, end_str in TIME_BLOCKS:
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
        if start_time <= now <= end_time:
            return True
    return False

def notify(title, msg):
    current_time = datetime.now().strftime('%I:%M %p')
    full_msg = f"{msg}\n{current_time}"
    notifier.show_toast(title, full_msg, duration=5, threaded=True)
    threading.Thread(target=show_popup, args=(title, full_msg), daemon=True).start()

def countdown(seconds):
    start = time.time()
    while running and time.time() - start < seconds:
        time.sleep(1)

def timer_loop():
    global running
    while running:
        if in_time_block():
            notify("🧠 Work Time", "Focus now!")
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
    # Keep main thread alive
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
