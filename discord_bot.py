from typing import Final
from texttoollama import clear_memorys
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import re

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
        print(e)



# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

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
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
    
# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)
    
    
@client.command(pass_context=True)
async def join(ctx):
    voice_channel = ctx.author.voice.channel 
    if voice_channel is None:
        await ctx.send("please join a voice channel first")
        return
    await play_audio(voice_channel, "Papers, Please Theme Song - dukope1.mp3")
    
async def play_audio(voice_channel, audio):
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(audio, executable="B:/ffmpeg/bin/ffmpeg.exe"))
    while vc.is_playing():
        await asyncio.sleep(1)  
    await vc.disconnect()


        
@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.voice_client.disconnect()
        
    else:
        await ctx.send("I am not connected to a voice channel.")


if __name__ == '__main__':
    import asyncio
    client.run(token=TOKEN)

