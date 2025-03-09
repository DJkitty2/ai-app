from TTS.utils.manage import ModelManager

def list_tts_voices():
    manager = ModelManager()
    models = manager.list_models()
    print("Available TTS Voices:")
    for model in models:
        print(f"- {model}")

if __name__ == "__main__":
    list_tts_voices()