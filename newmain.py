from RealtimeSTT import AudioToTextRecorder
from texttoollama import get_llama_response
import re
import os
import sounddevice as sd
import numpy as np
import keyboard

def filter_thoughts(text):
    """Remove content inside <think> tags."""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()



def main():
    recorder = AudioToTextRecorder()
    name = os.name

    if name == "nt":
        key = "Insert"
        print(key)
    else:
        key = "Esc"
        print(key)

    print("Press " + key + " to record...")

    while True:
        """start recording"""
        keyboard.wait(key, suppress=True)
        recorder.start()
        """stop recording"""
        print("ready press " + key + " to stop")
        keyboard.wait(key, suppress=True)
        recorder.stop()
        """print recording"""
        print("Recording stopped.")
        print("Transcription:", recorder.text())
        """send to ollama"""
        recorder.text() = get_llama_response(text)

if __name__ == '__main__':
    main()