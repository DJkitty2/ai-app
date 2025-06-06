from texttoollama import get_llama_response
from texttospeach import speak_text
from RealtimeSTT import AudioToTextRecorder
import os
import keyboard
from timer2 import timer_start, timer_stop, timer_reset, timer_get
import pyautogui

def main():

    name = os.name
    
    if name == "nt":
        record_key = "Insert"
        print("small")
        recorder = AudioToTextRecorder(model="small", language="en", spinner=True, device="cuda")
    else:
        record_key = "Esc"
        print("tiny")
        recorder = AudioToTextRecorder(model="tiny", language="en", spinner=True)
    print(f"Press {record_key} to start/stop recording.")

    while True:

        """Start recording"""
        keyboard.wait(record_key, suppress=True)
        recorder.start()
        print("Recording started...")

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
        response_text = response.content if hasattr(response, "content") else response
        print("Response:", response_text)
        timer_stop()
        print(f"Response time: {timer_get()} seconds")
        timer_reset()

        #time.sleep(3)
        
        """Filter out thoughts and speak"""
        speak_text(response_text)
        #pyautogui.typewrite(f"{response_text} \n \n", interval=0.01) # one or the other

if __name__ == "__main__":
    main()
