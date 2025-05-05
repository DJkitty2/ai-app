from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

url = "https://www.youtube.com/watch?v=CDnT4uEKnww"

yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)

ys = yt.streams.get_audio_only()
ys.download()

os.rename(ys.default_filename, "audio.mp4a")