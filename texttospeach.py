import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    sample_text = "Hello! This is a test message."
    speak_text(sample_text)
