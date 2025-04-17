
# FocusFlow Timer

FocusFlow is a lightweight **Windows timer app** that helps you stay productive by following the Pomodoro technique, where you work for a set time followed by short breaks. The app runs in the background, notifies you when a new work or rest period begins, and displays a custom popup even if Windows **Do Not Disturb** (DND) mode is active.

---

## Features

- **Work and Rest Time**: Customizable work/rest intervals (e.g., 25 minutes work, 5 minutes break).
- **Multiple Time Blocks**: Set multiple work periods during the day (e.g., 9 AM - 1 PM, 5 PM - 9 PM).
- **System Tray Icon**: A tray icon that lets you quit the app at any time.
- **Windows Notifications**: Toast notifications and fallback popups to notify the user.
- **Configurable Settings**: Easily change work and rest intervals via `config.json`.

---

## Requirements

- **Python 3.6+**
- **Libraries**:
  - `pystray` - For the system tray icon.
  - `win10toast` - For showing Windows toast notifications.
  - `pyinstaller` - To create the `.exe` file.
  - `Pillow` - For image manipulation (tray icon).
  - `ctypes` - To use native Windows message boxes for fallback notifications.
  
You can install these dependencies using the following command:

```bash
pip install pystray win10toast pyinstaller Pillow
```

---

## Installation and Usage

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/ArulVirumbi/FocusFlow.git
```

### 2. Modify `config.json`

You can configure your work and rest times in the `config.json` file.

Example `config.json`:

```json
{
    "work_duration_min": 25,
    "rest_duration_min": 5,
    "time_blocks": [
        {"start": "09:00", "end": "13:00"},
        {"start": "17:00", "end": "21:00"}
    ]
}
```

- **`work_duration_min`**: Duration of work time in minutes.
- **`rest_duration_min`**: Duration of rest time in minutes.
- **`time_blocks`**: Time blocks during the day when the timer should be active.

### 3. Run the app

To run the app, execute the Python script directly:

```bash
python focusflow.py
```

This will:
- Start the timer loop based on your `config.json`.
- Show a system tray icon and notify you during work/rest intervals.
- Show a popup when a work/rest period begins or ends.

### 4. Convert to `.exe` (Optional)

To convert the script into a standalone `.exe` for easier distribution on Windows, use **PyInstaller**.

Run the following command in your terminal:

```bash
pyinstaller --noconsole --onefile --add-data "config.json;." focusflow.py
```

This will generate a `.exe` file in the `dist/` folder that you can run directly on any Windows machine. Ensure that `config.json` is included in the same folder as the `.exe`.

---

## How to Customize

### 1. Change Work and Rest Times

You can adjust the following settings in the `config.json` file:
- **`work_duration_min`**: The number of minutes to work before taking a break.
- **`rest_duration_min`**: The number of minutes to take a break before starting another work period.

Example:

```json
{
    "work_duration_min": 30,
    "rest_duration_min": 10
}
```

### 2. Add More Time Blocks

You can add more time blocks in the `time_blocks` list to specify different work periods during the day. 

For example:

```json
{
    "time_blocks": [
        {"start": "08:00", "end": "12:00"},
        {"start": "14:00", "end": "18:00"}
    ]
}
```

---

## How It Works

- **Main Timer Loop**: The app checks if the current time is within a defined time block (`09:00 - 13:00`, etc.). If it is, the timer counts down the work period, then the rest period.
- **Notifications**: The app uses both **Windows toast notifications** and **fallback popups** that will show up even if **Do Not Disturb (DND)** mode is enabled.
- **System Tray**: The app runs silently in the background with a system tray icon. Right-click the icon to quit the app.

---

## Troubleshooting

1. **Popup not disappearing**: 
   - If the popup is not disappearing after 5 seconds, ensure you're using the `MessageBoxTimeoutW` function correctly in the code. The popup should close after the set timeout.

2. **Error `WNDPROC return value cannot be converted to LRESULT`**:
   - This error is generally safe to ignore — it’s related to the internal workings of `pystray`. The app still functions normally.

3. **Windows Defender warning**:
   - If Windows Defender or another antivirus flags the `.exe` file, you can ignore this warning or sign the `.exe` for authenticity.

---

## Contributing

Feel free to open issues or submit pull requests if you'd like to improve the app.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
