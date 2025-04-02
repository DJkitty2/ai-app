from RealtimeSTT import AudioToTextRecorder
from texttoollama import get_llama_response
from texttospeach import speak_text
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

    recorder.start()
    if name == "nt":
        record_key = "Insert"
        exit_key = "Ctrl+Esc"
    else:
        record_key = "Esc"
        exit_key = "Ctrl+Esc"

    print(f"Press {record_key} to start/stop recording, or {exit_key} to exit...")

    while True:
        """Start recording"""
        keyboard.wait(record_key, suppress=True)
        print("Recording started...")
        recorder.start()

        """Stop recording"""
        print(f"Press {record_key} to stop recording...")
        keyboard.wait(record_key, suppress=True)
        recorder.stop()
        print("Recording stopped.")

        """Print transcription"""
        transcription = recorder.text()
        print("Transcription:", transcription)

        """Send to Llama"""
        print("Sending to Llama...")
        response = get_llama_response(transcription)
        response_text = response.content if hasattr(response, 'content') else response
        print("Response:", response_text)

        """Filter out thoughts and speak"""
        filtered_text = filter_thoughts(response_text)
        speak_text(filtered_text)

        """Check for exit key"""
        print(f"Press {exit_key} to exit or {record_key} to record again...")
        if keyboard.is_pressed(exit_key):
            print("Exiting...")
            break

if __name__ == '__main__':
    main()