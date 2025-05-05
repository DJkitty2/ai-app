from texttoollama import get_llama_response
from timer2 import timer_start, timer_stop, timer_reset, timer_get
import re
import asyncio

def filter_thoughts(text):
    """Remove content inside <think> tags."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

async def get_response(username: str, user_input: str, channel: str) -> str: 
    lowered: str = user_input.lower()    
    try:
        timer_reset()
        timer_start()
        # Use asyncio.to_thread to run the synchronous function in a thread
        response = await asyncio.to_thread(get_llama_response, f"{user_input} said {username} in {channel} on discord")
        filtered = filter_thoughts(response)
        timer_stop()
        print(f"Response time: {timer_get()} seconds")
        return filtered + f" \n\n to {user_input}"
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request at the moment."