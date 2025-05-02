from typing import Final
from texttoollama import clear_memorys
import os
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
    


if __name__ == '__main__':
    main()


