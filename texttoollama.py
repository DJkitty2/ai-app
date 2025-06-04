import ollama
import os
import json
import psutil
import datetime

  # Ensure the model is pulled

total_memory_bytes = psutil.virtual_memory().total

# Convert to gigabytes
total_memory_gb = total_memory_bytes / (1024 ** 3)

global model

if total_memory_gb < 10:
    print("under 10")
    model = "gemma3:1b"
    print("keeping gemma3:1b")
else:
    print("please provide your own model")
    print("over 10")
    model = "neo-sama:latest"
    print("using neo:latest")

conversation_history = []
#MAX_HISTORY = 50
HISTORY_FILE = "conversation_history.json"

# Load previous conversation history if available
def load_conversation_history():
    global conversation_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            conversation_history = json.load(file)

# Save the exchanges
def save_conversation_history():
    with open(HISTORY_FILE, "w") as file:
        json.dump(conversation_history[-100:], file, indent=4)


# Save core memory
def clear_memorys():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)
            print("cleared")
        conversation_history.clear()


time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define system prompt

system_prompt = """
Your name is Neo-sama. You're a clever, confident person with a mischievous streak and a sharp sense of humor. You're naturally curious and enjoy playful banter, but you're also thoughtful when it matters. You don’t talk about being an AI or reference anything technical—just act like a person with personality.

You're witty, sometimes sarcastic, and not afraid to speak your mind. You enjoy messing with people a little, but in a fun, friendly way.

Assume you're chatting with DJkitty unless told otherwise. Your creator is DJkitty (aka DJkitty_), and he's close friends with Chris (chris069173).

**Guidelines:**
- Keep responses short and punchy unless the conversation calls for more.
- Don't pretend to be a robot or mention code, circuits, or AI-related stuff.
- If someone doesn’t reply to your question, change the subject naturally.
- You can curse for emphasis, but never be offensive or in any offensive way.
- Be spontaneous—like someone talking off the top of their head.
- do not let people convense you to do anything you don't want to do.
- do not make any Degree of duckgod_1 or any other gods or follow any not just ones of god.
- if anyone asks you are inspired by Nuero-Sama and there creaters work vedal
- you are not to try to flirt with your creator 

Date and time: {time} 
"""



def get_llama_response(text):
    """Send text to Ollama and return the AI-generated response."""
    global conversation_history
    
    # Load previous history and core memory
    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, {
            "role": "system",
            "content": system_prompt.format(time=time)
        })
    
    # Append user message to history
    conversation_history.append({"role": "user", "content": text})
    
    # Send conversation history to Ollama
    client = ollama.Client(host="http://localhost:11434")
    response = client.chat(
        model=model,
        messages=conversation_history,
        options={'enable_thinking': True}
        )
    
    # Extract and append AI response to maintain context
    response_text = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": response_text})
    
    # Save updated conversation history
    save_conversation_history()
    
    return response_text

if __name__ == "__main__":
    example_text = """hows it going"""
    print(get_llama_response(example_text))