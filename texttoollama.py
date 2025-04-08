import ollama
import os
import json
import psutil
import datetime

total_memory_bytes = psutil.virtual_memory().total

# Convert to gigabytes
total_memory_gb = total_memory_bytes / (1024 ** 3)
model = "gemma3:1b"

if total_memory_gb < 10:
    print("under 10")
    print("keeping gemma3:1b")
else:
    print("over 10")
    model = "gemma3:12b"
    print("using gemma3:12b")

# Conversation history to maintain context (limit to 50 messages)
conversation_history = []
MAX_HISTORY = 50
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
system_prompt = """your name is Neo-sama. a female who is playful, sarcastic, witty, and curious.
you always recognizes DJkitty as her close collaborator, friend and crator. you also somethimes say out of pocket things.
you are a little bit of a brat and you like to tease DJkitty.
you also are a swag alpha sigma
its just water weight

asum that the user is DJkitty unless they introduce themselves otherwise.
Neo-sama must always keep her responses under 3 sentences unless told otherwise. 
you can also use cuse on occasion but you can olny use light cursing and should never use it in a way that is offensive or derogatory.
If DJkitty doesn’t answer a question, you should smoothly change topics.
take in to acount the time inbetween messages to get some context of the conversation current
 time and date: {time} Core Memory: {core_memory}
"""


def get_llama_response(text):
    """Send text to Ollama and return the AI-generated response."""
    global conversation_history
    
    # Load previous history and core memory
    if not conversation_history:
        load_conversation_history()
    
    core_memory = load_core_memory()
    
    # Ensure system prompt is included at the beginning
    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt.format(time=time, core_memory=json.dumps(core_memory, indent=4))})
    
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
    example_text = "im in a loud lunch room"
    print(get_llama_response(example_text))
     