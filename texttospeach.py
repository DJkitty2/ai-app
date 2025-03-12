from TTS.api import TTS
import simpleaudio as sa

def speak_text(text):
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", progress_bar=True, gpu=False)
    tts.tts_to_file(text=text, file_path="output.wav")

    # Play the audio
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

if __name__ == "__main__":
    sample_text = "sigma sigma boy sigma boy."
    speak_text(sample_text)

