import keyboard
import pyttsx3
from voicetotext import transcribe_audio
from texttoollama import get_llama_response

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

while True:
    if keyboard.read_key() == "p":
        text = transcribe_audio("C:\Users\DJkitty\Desktop\ai app\audio.mp3")
        response = get_llama_response(text)
        engine.say(response)  # Concatenate the strings
        print("Ollama's Response:", response)
        print("You pressed p")
        engine.runAndWait()  # This line is necessary to actually produce speech