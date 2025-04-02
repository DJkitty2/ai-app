from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)



def transcribe_audio():
    """Transcribe audio from the microphone."""
    recorder = AudioToTextRecorder()
    print("ready")
    recorder.start()
    print("Recording started...")
    input("Press Enter to stop recording...")
    recorder.stop()
    print("Recording stopped.")
    print("Transcription:", recorder.text())

