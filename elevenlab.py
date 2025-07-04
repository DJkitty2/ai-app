import elevenlabs 
import os
from pydub import AudioSegment
from pydub.playback import play

api_key = os.getenv('ELEVENLABS_API_KEY')
voice_id = os.getenv('AGENT_ID')

elevenlabs.set_api_key(api_key)

def speak_text(text):
    audio = elevenlabs.generate(
        text=text,
        voice = voice_id
    )
    elevenlabs.play(audio)
    elevenlabs.save(audio, "output.mp3")