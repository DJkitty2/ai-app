import re
from TTS.api import TTS
import simpleaudio as sa

def clean_text(text):
    """Remove non-ASCII characters from the input text."""
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Keeps only standard ASCII characters

def speak_text(text):
    text = clean_text(text)  # Clean text before passing to TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", progress_bar=True, gpu=False)
    tts.tts_to_file(text=text, file_path="output.wav")

    # Play the audio
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    sample_text = "this is a test mesige!"
    speak_text(sample_text)
