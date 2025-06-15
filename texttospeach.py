import simpleaudio as sa
import re
import os
import torch
import soundfile as sf
from kokoro_onnx import Kokoro


if os.name == "nt":
    device = "cuda" if torch.cuda.is_available() else "cpu"
else:
    device = "cpu"
    
def filter_thoughts(text):
    """Remove content inside <think> tags."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def clean_text(text):
    """Remove non-ASCII characters from the input text."""
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Keeps only standard ASCII characters

def speak_text(text):
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    samples, sample_rate = kokoro.create(
        text=text, voice="af_sarah", speed=1.0, lang="en-us"
    )
    sf.write("output.wav", samples, sample_rate)
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    sample_text = """AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
    speak_text(sample_text)
 