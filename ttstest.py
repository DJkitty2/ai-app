from RealtimeSTT import AudioToTextRecorder

def main():
    recorder = AudioToTextRecorder(
        model="tiny",
        language="en",
        spinner=True,
        wakeword_backend="openwakeword",
        wake_words="jarvis"
    )

if __name__ == "__main__":
    main()