import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("base")  # Load model
    result = model.transcribe(file_path)
    return result["text"]  # Return the transcribed text

# Only run this if the script is executed directly
if __name__ == "__main__":
    text = transcribe_audio("recorded_audio.wav")
    print(text)
