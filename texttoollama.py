import ollama
import os
import json
import psutil
import datetime

file_path = 'system_prompt.txt'
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
            return json.load(file)
    return {"example_fact": "DJkitty loves AI experiments"}  # Default example

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

with open(file_path, 'r') as file: 
    file_content = file.read()
# Define system prompt
system_prompt = file_content + f" current time and date: {time} Core Memory: {load_core_memory()}"


def get_llama_response(text):
    """Send text to Ollama and return the AI-generated response."""
    global conversation_history
    
    # Load previous history and core memory
    if not conversation_history:
        load_conversation_history()
    
    core_memory = load_core_memory()
    
    # Ensure system prompt is included at the beginning
    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt.format(core_memory=json.dumps(core_memory, indent=4))})
    
    # Append user message to history
    conversation_history.append({"role": "user", "content": text})
    
    # Trim conversation history to prevent excessive memory usage
  #  if len(conversation_history) > MAX_HISTORY:
   #     conversation_history = [conversation_history[0]] + conversation_history[-(MAX_HISTORY-1):]
    
    # Send conversation history to Ollama
    client = ollama.Client(host="http://localhost:11434")
    response = client.chat(
        model=""+model+"", 
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
    example_text = "Hello, how are you?"
    print(get_llama_response(example_text))
