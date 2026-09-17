# Hello Hand App (Simple Version) — Setup with a Virtual Environment

Running inside a venv keeps these packages isolated from your system Python.

## 1. Copy the file to the Pi
Save `hello_hand_app.py` to `/home/pi/hello_hand_app.py`.

## 2. Install system packages (needed before creating the venv)
These are OS-level libraries the Python packages depend on — they go outside the venv:
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-tk portaudio19-dev flac -y
```

## 3. Create and activate the virtual environment
```bash
cd /home/pi
python3 -m venv --system-site-packages hello_hand_env
source hello_hand_env/bin/activate
```
`--system-site-packages` is important here — `tkinter` and GPIO access work more
reliably when the venv can see the system-installed packages too. Your prompt
should now show `(hello_hand_env)` at the start of the line.

## 4. Install Python packages inside the venv
```bash
pip install SpeechRecognition pyaudio gpiozero
```

## 5. Wire the servo
- Signal wire -> GPIO18 (BCM numbering) on the Pi, or change `SERVO_PIN` in the script
- Power the servo from a separate 5-6V supply, NOT the Pi's 5V pin
- Connect the servo's ground and the Pi's ground together (common ground)

## 6. Test it (venv still activated)
```bash
python hello_hand_app.py
```
Click "Test Hand Raise" first, then "Start Listening" and say "hello".

## 7. Make it a desktop app that auto-activates the venv
The `.desktop` launcher needs to run the venv's Python directly (no manual
activation needed) — use `HelloHandApp.desktop` as provided, which points to:
```
Exec=/home/pi/hello_hand_env/bin/python /home/pi/hello_hand_app.py
```
If your username isn't `pi`, edit both paths in the file accordingly.

Then:
```bash
cp HelloHandApp.desktop ~/Desktop/
chmod +x ~/Desktop/HelloHandApp.desktop
```
Right-click the icon → "Allow Launching" the first time, then double-click to run.

## 8. (Optional) Auto-start on boot
```bash
mkdir -p ~/.config/autostart
cp HelloHandApp.desktop ~/.config/autostart/
```

## Everyday use
Each time you want to run it manually from the terminal:
```bash
source /home/pi/hello_hand_env/bin/activate
python /home/pi/hello_hand_app.py
```
The desktop icon does NOT need this — it calls the venv's Python directly.

## Notes
- Needs internet (Google's free speech API), no account or key required.
- If `gpiozero` has trouble accessing GPIO pins from inside the venv, run the
  app with `sudo` or add your user to the `gpio` group:
  `sudo usermod -aG gpio $USER` (then log out and back in).
