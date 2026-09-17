#!/usr/bin/env python3
"""
Hello Hand App (Simple Version)
--------------------------------
Listens to the microphone. When it hears "hello", raises a servo-controlled
hand, then lowers it again. No API key, no cost, no chat — just detection
and a servo move.

Run it directly:
    python3 hello_hand_app.py

Or double-click the HelloHandApp.desktop launcher (see SETUP.md).
"""

import threading
import tkinter as tk
from tkinter import ttk
from time import sleep

import speech_recognition as sr
from gpiozero import AngularServo

# ----------------------------------------------------------------------
# CONFIG — adjust these for your setup
# ----------------------------------------------------------------------
SERVO_PIN = 18            # BCM GPIO pin the servo signal wire is connected to
SERVO_MIN_ANGLE = 0        # rest position
SERVO_MAX_ANGLE = 90       # raised position
SERVO_MIN_PULSE = 0.0005
SERVO_MAX_PULSE = 0.0025

TRIGGER_WORD = "hello"

# ----------------------------------------------------------------------
# SERVO CONTROL
# ----------------------------------------------------------------------
hand_servo = AngularServo(
    SERVO_PIN,
    min_angle=SERVO_MIN_ANGLE,
    max_angle=SERVO_MAX_ANGLE,
    min_pulse_width=SERVO_MIN_PULSE,
    max_pulse_width=SERVO_MAX_PULSE,
)


def raise_hand():
    hand_servo.angle = SERVO_MAX_ANGLE
    sleep(1.5)
    hand_servo.angle = SERVO_MIN_ANGLE


# ----------------------------------------------------------------------
# LISTENING (free, local mic + Google's free speech API — no key needed)
# ----------------------------------------------------------------------
class Listener:
    def __init__(self, on_heard, on_status):
        self.on_heard = on_heard
        self.on_status = on_status
        self._running = False
        self._thread = None
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        with self.mic as source:
            self.on_status("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.on_status("Listening...")

            while self._running:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    text = self.recognizer.recognize_google(audio).lower()
                    self.on_heard(text)

                    if TRIGGER_WORD in text:
                        self.on_status("Heard 'hello' — raising hand")
                        raise_hand()
                        self.on_status("Listening...")

                except sr.WaitTimeoutError:
                    pass  # no speech in the timeout window, just keep listening
                except sr.UnknownValueError:
                    pass  # heard something but couldn't understand it
                except sr.RequestError as e:
                    self.on_status(f"Network error: {e}")
                except Exception as e:
                    self.on_status(f"Error: {e}")


# ----------------------------------------------------------------------
# GUI
# ----------------------------------------------------------------------
class HelloHandApp:
    def __init__(self, root):
        self.root = root
        root.title("Hello Hand App")
        root.geometry("400x230")

        self.status_var = tk.StringVar(value="Stopped")
        self.heard_var = tk.StringVar(value="")

        ttk.Label(root, text="Hello Hand App", font=("Helvetica", 18, "bold")).pack(pady=10)

        ttk.Label(root, textvariable=self.status_var, font=("Helvetica", 12)).pack(pady=5)

        ttk.Label(root, text="Last heard:").pack(pady=(10, 0))
        ttk.Label(root, textvariable=self.heard_var, wraplength=360, justify="center").pack(pady=5)

        self.toggle_button = ttk.Button(root, text="Start Listening", command=self.toggle)
        self.toggle_button.pack(pady=15)

        ttk.Button(root, text="Test Hand Raise", command=raise_hand).pack()

        self.listener = Listener(on_heard=self.update_heard, on_status=self.update_status)
        self.listening = False

    def toggle(self):
        if not self.listening:
            self.listener.start()
            self.listening = True
            self.toggle_button.config(text="Stop Listening")
        else:
            self.listener.stop()
            self.listening = False
            self.toggle_button.config(text="Start Listening")
            self.update_status("Stopped")

    def update_status(self, text):
        self.root.after(0, lambda: self.status_var.set(text))

    def update_heard(self, text):
        self.root.after(0, lambda: self.heard_var.set(text))


if __name__ == "__main__":
    root = tk.Tk()
    app = HelloHandApp(root)
    root.mainloop()
