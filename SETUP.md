# Hello Hand App (Simple Version) — Setup on Raspberry Pi OS

No API key, no OpenAI, no cost. Uses your microphone + Google's free speech
recognition (needs internet, but no account or key) to detect the word
"hello" and move a servo.

## 1. Copy the file to the Pi
Save `hello_hand_app.py` to `/home/pi/hello_hand_app.py`.

## 2. Install dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-tk portaudio19-dev flac -y
pip3 install SpeechRecognition pyaudio gpiozero
```
(`flac` is needed by SpeechRecognition to encode audio for the free API.)

## 3. Wire the servo
- Signal wire -> GPIO18 (BCM numbering) on the Pi, or change `SERVO_PIN` in the script
- Power the servo from a separate 5-6V supply, NOT the Pi's 5V pin
- Connect the servo's ground and the Pi's ground together (common ground)

## 4. Test it from the terminal first
```bash
python3 /home/pi/hello_hand_app.py
```
Click "Test Hand Raise" first to confirm the servo moves correctly.
Then click "Start Listening" and say "hello" — watch the "Last heard" text
to confirm your mic and internet connection are working.

## 5. Make it a real desktop app
1. Edit `HelloHandApp.desktop` and fix the `Exec=` path if your username isn't `pi`.
2. Copy it to your Desktop:
   ```bash
   cp HelloHandApp.desktop ~/Desktop/
   chmod +x ~/Desktop/HelloHandApp.desktop
   ```
3. Right-click the icon → "Allow Launching" (Raspberry Pi OS asks this once).
4. Double-click the icon — the app opens with a Start/Stop button.

## 6. (Optional) Auto-start on boot
```bash
mkdir -p ~/.config/autostart
cp HelloHandApp.desktop ~/.config/autostart/
```

## Notes
- This needs an internet connection (Google's free speech API), but no account or key.
- If you want it to work fully offline (no internet at all), let me know — that
  needs a different, heavier local model (like `vosk`) instead.
- If your servo is driven through a PCA9685 board instead of a direct GPIO pin,
  tell me and I'll adjust the servo control code.
