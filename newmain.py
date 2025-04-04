from RealtimeSTT import AudioToTextRecorder
from texttoollama import get_llama_response
from texttospeach import speak_text
import re
import os
import sounddevice as sd
import numpy as np
import keyboard
from timer import timer_start, timer_stop, timer_reset, timer_get
import time

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
        timer_start()
        print("Sending to Llama...")
        response = get_llama_response(transcription)
        response_text = response.content if hasattr(response, 'content') else response
        print("Response:", response_text)
        timer_stop()
        print(f"Response time: {timer_get()} seconds")
        timer_reset()

        time.sleep(3) #remove this line if you want to remove the delay for debugging

        """Filter out thoughts and speak"""
        timer_start()
        filtered_text = filter_thoughts(response_text)
        speak_text(filtered_text)
        timer_stop()
        print(f"Speak time: {timer_get()} seconds")
        timer_reset()
        
        """Check for exit key"""
        print(f"Press {exit_key} to exit or {record_key} to record again...")
        if keyboard.is_pressed(exit_key):
            print("Exiting...")
            break

if __name__ == '__main__':
    main()