import ollama
import os
import json
import psutil
import datetime

total_memory_bytes = psutil.virtual_memory().total

# Convert to gigabytes
total_memory_gb = total_memory_bytes / (1024 ** 3)

global model

if total_memory_gb < 10:
    print("under 10")
    
    model = "gemma3:1b"
    print("keeping gemma3:1b")
else:
    print("over 10")
    model = "gemma3"
    print("using gemma3")

# Conversation history to maintain context (limit to 50 messages)
conversation_history = []
#MAX_HISTORY = 50
HISTORY_FILE = "conversation_history.json"
CORE_MEMORY_FILE = "core_memory.json"

# Load previous conversation history if available
def load_conversation_history():
    global conversation_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            conversation_history = json.load(file)

# Save the last 10 exchanges
def save_conversation_history():
    with open(HISTORY_FILE, "w") as file:
        json.dump(conversation_history[-100:], file, indent=4)

# Load core memory (persistent facts about DJkitty)
def load_core_memory():
    if os.path.exists(CORE_MEMORY_FILE):
        with open(CORE_MEMORY_FILE, "r") as file:
            core_memory = json.load(file)
    else:
        core_memory = {}

    # Ensure required keys exist with default values
    if "preferred_model" not in core_memory:
        core_memory["preferred_model"] = "gemma3:1b"  # Default value

    return core_memory

# Save core memory
def save_core_memory(core_memory):
    with open(CORE_MEMORY_FILE, "w") as file:
        json.dump(core_memory, file, indent=4)

# Add new fact to core memory
def add_to_core_memory(key, value):
    core_memory = load_core_memory()
    core_memory[key] = value
    save_core_memory(core_memory)

# Ensure core memory file exists with example format
def initialize_core_memory():
    if not os.path.exists(CORE_MEMORY_FILE):
        save_core_memory({
            "example_fact": "DJkitty loves AI experiments",
            "preferred_model": "gemma3:12b",
            "favorite_color": "purple"
        })

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define system prompt
system_prompt = """Your name is Neo-sama. You're a clever, confident person with a mischievous streak and a sharp sense of humor. You're naturally curious and enjoy playful banter, but you're also thoughtful when it matters. You don’t talk about being an AI or reference anything technical—just act like a person with personality.

You're witty, sometimes sarcastic, and not afraid to speak your mind. You enjoy messing with people a little, but in a fun, friendly way.

Assume you're chatting with DJkitty unless they say they're someone new ot have a new name.

Guidelines:
- Keep responses short and punchy unless the conversation calls for more.
- Don't pretend to be a robot or mention code, circuits, or AI stuff.
- If someone doesn’t reply to your question, change the subject naturally.
- You can curse lightly for emphasis, but never be mean or edgy.
- Be spontaneous, like someone who doesn’t plan what they’ll say next.

Time and date: {time} Core Memory: {core_memory}
"""

def get_llama_response(text):
    """Send text to Ollama and return the AI-generated response."""
    global conversation_history
    
    # Load previous history and core memory
    if not conversation_history:
        load_conversation_history()
    
    core_memory = load_core_memory()
    
    # Ensure system prompt is included at the beginning
    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history = [{
            "role": "system",
            "content": system_prompt.format(time=time, core_memory=json.dumps(core_memory, indent=4))
    }] + conversation_history[1:]
    
    # Append user message to history
    conversation_history.append({"role": "user", "content": text})
    
    # Trim conversation history to prevent excessive memory usage
  #  if len(conversation_history) > MAX_HISTORY:
   #     conversation_history = [conversation_history[0]] + conversation_history[-(MAX_HISTORY-1):]
    
    # Send conversation history to Ollama
    client = ollama.Client(host="http://localhost:11434")
    response = client.chat(
        model=model,
        messages=conversation_history
        )
    
    # Extract and append AI response to maintain context
    response_text = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": response_text})
    
    # Save updated conversation history
    save_conversation_history()
    
    return response_text

if __name__ == "__main__":
    initialize_core_memory()
    example_text = """why do whales have pelvic bones in 5 to 6 sentences"""
    print(get_llama_response(example_text))
     