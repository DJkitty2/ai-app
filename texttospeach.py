import re
import pyttsx3
import RealtimeTTS
import TTS

def clean_text(text):
    """Remove non-ASCII characters from the input text."""
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Keeps only standard ASCII characters

def speak_text(text, voice_name=None):
    text = clean_text(text)  # Clean text before passing to TTS

    engine = pyttsx3.init()

    if voice_name:
        voices = engine.getProperty('voices')
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    # Use RealtimeTTS.speak() instead of trying to instantiate it
    RealtimeTTS.speak(text)
    tts.speak(text)

if __name__ == "__main__":
    sample_text = "Hello! This is Siri's voice using RealtimeTTS."
    speak_text(sample_text, voice_name="Samantha")  # Change to your preferred Siri voice
