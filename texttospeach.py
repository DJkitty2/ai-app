from TTS.api import TTS
import simpleaudio as sa
import re
import os
import torch

if os.name == "nt":
    device = "cuda" if torch.cuda.is_available() else "cpu"
else:
    device = "cpu"

def clean_text(text):
    """Remove non-ASCII characters from the input text."""
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Keeps only standard ASCII characters

def speak_text(text):
    text = clean_text(text)  # Clean text before passing to TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True)
    tts.to(device)
    tts.tts_to_file(
        text=text,
        file_path="output.wav"
        )
    
    
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    sample_text = """hello, this is a test of the text-to-speech system. Let's see how it handles this text!"""
    speak_text(sample_text)
 