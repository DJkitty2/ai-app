from voicetotext import transcribe_audio
from texttoollama import get_llama_response
from texttospeach import speak_text
import re
import os

name = os.name

if name == "nt":
    key = Insert
    print(key)
else:
    key = "Esc"
    print(key)

def record_audio(audio_file):
    import sounddevice as sd
    import numpy as np
    import wave
    import keyboard

    
    
    SAMPLE_RATE = 44100  # CD-quality audio
    CHANNELS = 1  # Mono audio

    print("Press and hold "+key+" to record...")
    while not keyboard.is_pressed(key):
        pass  # Wait for key press
    print("Recording started...")

    frames = []
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16', device=None) as stream:
        while keyboard.is_pressed(key):
            data, _ = stream.read(1024)
            frames.append(data)

    print("Recording stopped.")

    if not frames:
        print("No audio recorded. Please try again.")
        return False

    # Convert frames to numpy array and save as WAV
    audio_data = np.concatenate(frames, axis=0)
    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    print("Recording saved.")
    return True

def filter_thoughts(text):
    """Remove content inside <think> tags."""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def main():
    while True:
        audio_file = "recorded_audio.wav"

        if record_audio(audio_file):
            text = transcribe_audio(audio_file)

            # Step 2: Send it to Ollama
            print("Send it to Ollama")
            response = get_llama_response(text)
            response_text = response.content if hasattr(response, 'content') else str(response)

            # Step 3: Print or use the response
            print("Ollama's Response:", response_text)

            # Step 4: Filter and convert response text to speech
            print("Filter and convert response text to speech")
            filtered_text = filter_thoughts(response_text)
            speak_text(filtered_text)

if __name__ == "__main__":
    main()
