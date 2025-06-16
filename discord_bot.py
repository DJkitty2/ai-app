from typing import Final
from texttoollama import clear_memorys
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responces import get_response
import re
from pytubefix import YouTube
from pytubefix.cli import on_progress  # Import Pytube-specific exceptions

def filter_thoughts(text):
    """Remove content inside <think> tags."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
CHANNEL: Final[int] = int(os.getenv('DISCORD_CHANNEL'))

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client = commands.Bot(command_prefix='!', intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    username: str = str(message.author)
    channel: str = str(message.channel)
    
    try:
        if message.channel.id != CHANNEL and not isinstance(message.channel, discord.DMChannel):
            return
        else:
            if is_private:
                # No typing indicator for DMs (optional)
                response: str = get_response(user_message, username, channel)
                await message.author.send(response)
            else:
                async with message.channel.typing():
                    response: str = get_response(user_message, username, channel)
                    await message.channel.send(response)
    except Exception as e:
        print(f"Error: {e}")

# STEP 3: HANDLING THE STARTUP FOR OUR BOT

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    channel = client.get_channel(CHANNEL)  # Replace CHANNEL with your channel ID
    if channel:
        await channel.send("use !cmd to see commands")

@client.command()
async def clear(ctx) -> None:
    clear_memorys()
    await ctx.send('done cleared!')

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    await client.process_commands(message) 
    
    if message.content.startswith('!'):
        return

    if message.content == 'Farewell message removed.': # for carl bot
        return
    
    if message.content == '❌ **Missing argument `amount`**.':
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
    
# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)
       
async def play_audio(voice_channel, audio, volume=0.4):  # Default volume is 50%
    vc = await voice_channel.connect()
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio, executable="B:/ffmpeg/bin/ffmpeg.exe"))
    source.volume = volume  # Set the volume (0.0 to 1.0)
    vc.play(source)
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

@client.command(pass_context=True)
async def join(ctx, arg, volume: float = 0.5):  # Allow volume adjustment via command
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("Please join a voice channel first.")
        return
    if not (0.0 <= volume <= 1.0):  # Validate volume range
        await ctx.send("Volume must be between 0.0 and 1.0.")
        return
    await play_audio(voice_channel, arg, volume)
        
@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        if os.path.isfile("audio.mp4a"):
            os.remove("audio.mp4a")
        await ctx.voice_client.disconnect()
        
    else:
        await ctx.send("I am not connected to a voice channel.")
        
@client.command(pass_context=True)
async def songs(ctx):
    folder_path = "music"
    if not os.path.isdir(folder_path):
        await ctx.send(f"Error: '{folder_path}' is not a valid directory.")
        return

    music_files = [item.name for item in os.scandir(folder_path) if item.is_file()]
    if not music_files:
        await ctx.send("No music files found in the 'music' folder.")
    else:
        music_list = "\n".join(music_files)
        await ctx.send(f"Available songs:\n{music_list}")
        
@client.command(pass_context=True)
async def cmd(ctx):
    await ctx.send("!join <file_name> <volume 1 - 0>")
    await ctx.send("!leave leaves call")
    await ctx.send("!music lists music files")
    await ctx.send("!clear clears memory")
    await ctx.send("!ytube <url> <volume 1 - 0>")
    
@client.command(pass_context=True)
async def ytube(ctx, url, volume: float = 0.5):
    try:
        if not (0.0 <= volume <= 1.0):  # Validate volume range
            await ctx.send("Volume must be between 0.0 and 1.0.")
            return

        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        await ctx.send(f"Loading and playing: {yt.title}")
        
        ys = yt.streams.get_audio_only()
        downloaded_file = ys.download()  # This is a synchronous function, no 'await' needed

        # Rename the downloaded file to a consistent name
        audio_file = "audio.mp4a"
        os.rename(downloaded_file, audio_file)

        # Play the audio
        await play_audio(ctx.author.voice.channel, audio_file, volume)

        # Clean up the file after playback
        os.remove(audio_file)
    except Exception as e:
        print(f"Error: {e}")
        os.remove("audio.mp4a") if os.path.isfile("audio.mp4a") else None
        os.remove(f"{yt.title}.mp4a") if os.path.isfile(f"{yt.title}.mp4a") else None
        await ctx.send("An error occurred while processing the YouTube video.")


if __name__ == '__main__':
    import asyncio
    client.run(token=TOKEN)

