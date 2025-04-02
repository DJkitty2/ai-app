from ttstest import transcribe_audio
import re
import os
import sounddevice as sd
import numpy as np
import keyboard

name = os.name

if name == "nt":
    key = "Insert"
    print(key)
else:
    key = "Esc"
    print(key)

print("Press and hold "+key+" to record...")


while True:
    keyboard.wait(key, suppress=True)
    transcribe_audio()